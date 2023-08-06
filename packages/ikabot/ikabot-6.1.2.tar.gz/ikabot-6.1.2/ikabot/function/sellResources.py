#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import math
import json
import gettext
import traceback
from decimal import *
from ikabot.config import *
from ikabot.helpers.gui import *
from ikabot.helpers.tienda import *
from ikabot.helpers.botComm import *
from ikabot.helpers.varios import addDot
from ikabot.helpers.pedirInfo import read
from ikabot.helpers.signals import setInfoSignal
from ikabot.helpers.process import set_child_mode
from ikabot.helpers.planearViajes import waitForArrival

t = gettext.translation('sellResources', 
                        localedir, 
                        languages=idiomas,
                        fallback=True)
_ = t.gettext

def elegirCiudadComercial(ciudades_comerciales):
	print(_('In which city do you want to sell resources?\n'))
	for i, ciudad in enumerate(ciudades_comerciales):
		print('({:d}) {}'.format(i + 1, ciudad['name']))
	ind = read(min=1, max=len(ciudades_comerciales))
	return ciudades_comerciales[ind - 1]

def getStoreInfo(s, ciudad):
	params = {'view': 'branchOfficeOwnOffers', 'activeTab': 'tab_branchOfficeOwnOffers', 'cityId': ciudad['id'], 'position': ciudad['pos'], 'backgroundView': 'city', 'currentCityId': ciudad['id'], 'templateView': 'branchOfficeOwnOffers', 'currentTab': 'tab_branchOfficeOwnOffers', 'actionRequest': 'REQUESTID', 'ajax': '1'}
	resp = s.post(params=params, noIndex=True)
	return json.loads(resp, strict=False)[1][1][1]


def getOfertas(s, ciudad, recurso):
	if recurso == 0:
		recurso = 'resource'
	else:
		recurso = str(recurso)
	data = {'cityId': ciudad['id'], 'position': ciudad['pos'], 'view': 'branchOffice', 'activeTab': 'bargain', 'type': '333', 'searchResource': recurso, 'range': ciudad['rango'], 'backgroundView': 'city', 'currentCityId': ciudad['id'], 'templateView': 'branchOffice', 'currentTab': 'bargain', 'actionRequest': 'REQUESTID', 'ajax': '1'}
	resp = s.post(payloadPost=data)
	html = json.loads(resp, strict=False)[1][1][1]
	return re.findall(r'<td class=".*?">(.*?)<br/>\((.*?)\)\s*</td>\s*<td>(.*?)</td>\s*<td><img src=".*?"\s*alt=".*?"\s*title=".*?"/></td>\s*<td style="white-space:nowrap;">(\d+)\s*<img src=".*?"\s*class=".*?"/>.*?</td>\s*<td>(\d+)</td>\s*<td><a onclick="ajaxHandlerCall\(this\.href\);return false;"\s*href="\?view=takeOffer&destinationCityId=(\d+)&', html)

def venderAOfertas(s, ciudad, recurso, e):
	banner()

	matches = getOfertas(s, ciudad, recurso)

	if len(matches) == 0:
		print(_('No offers available.'))
		enter()
		return

	print(_('Which offers do you want to sell to?\n'))

	ofertas = []
	max_venta = 0
	profit    = 0
	for match in matches:
		city, user, cant, precio, dist, idDestino = match
		city = city.strip()
		cantidad = cant.replace(',', '').replace('.', '')
		cantidad = int(cantidad)
		msg = _('{} ({}): {} at {} each ({} in total) [Y/n]').format(city, user, addDot(cantidad), precio, addDot(int(precio)*cantidad))
		rta = read(msg=msg, values=['y', 'Y', 'n', 'N', ''])
		if rta.lower() == 'n':
			continue
		ofertas.append(match)
		max_venta += cantidad
		profit += cantidad * int(precio)
	banner()
	if len(ofertas) == 0:
		return

	disp_venta = ciudad['recursos'][recurso]
	vender = disp_venta if disp_venta < max_venta else max_venta

	print(_('\nHow much do you want to sell? [max = {}]').format(addDot(vender)))
	vender = read(min=0, max=vender)

	faltaVender = vender
	profit    = 0
	for oferta in ofertas:
		city, user, cant, precio, dist, idDestino = oferta
		city = city.strip()
		cantidad = cant.replace(',', '').replace('.', '')
		cantidad = int(cantidad)
		compra = cantidad if cantidad < faltaVender else faltaVender
		faltaVender -= compra
		profit += compra * int(precio)
	print(_('\nSell {} of {} for a total of {}? [Y/n]').format(addDot(vender), materials_names[recurso], addDot(profit)))
	rta = read(values=['y', 'Y', 'n', 'N', ''])
	if rta.lower() == 'n':
		return

	set_child_mode(s)
	e.set()

	info = _('\nI sell {} of {} in {}\n').format(addDot(vender), materials_names[recurso], ciudad['name'])
	setInfoSignal(s, info)
	try:
		do_it1(s, vender,  ofertas, recurso, ciudad)
	except:
		msg = _('Error in:\n{}\nCause:\n{}').format(info, traceback.format_exc())
		sendToBot(s, msg)
	finally:
		s.logout()

def crearOferta(s, ciudad, recurso, e):
	banner()

	html = getStoreInfo(s, ciudad)
	cap_venta = getstorageCapacityDeVenta(html)
	recurso_disp = ciudad['recursos'][recurso]
	print(_('How much do you want to sell? [max = {}]').format(addDot(recurso_disp)))
	vender = read(min=0, max=recurso_disp)
	if vender == 0:
		return

	precio_max, precio_min = re.findall(r'\'upper\': (\d+),\s*\'lower\': (\d+)', html)[recurso]
	precio_max = int(precio_max)
	precio_min = int(precio_min)
	print(_('\nAt what price? [min = {:d}, max = {:d}]').format(precio_min, precio_max))
	precio = read(min=precio_min, max=precio_max)

	print(_('\nI will sell {} of {} at {}: {}').format(addDot(vender), materials_names[recurso], addDot(precio), addDot(precio * vender)))
	print(_('\nProceed? [Y/n]'))
	rta = read(values=['y', 'Y', 'n', 'N', ''])
	if rta.lower() == 'n':
		return

	set_child_mode(s)
	e.set()

	info = _('\nI sell {} of {} in {}\n').format(addDot(vender), materials_names[recurso], ciudad['name'])
	setInfoSignal(s, info)
	try:
		do_it2(s, vender, precio, recurso, cap_venta, ciudad)
	except:
		msg = _('Error in:\n{}\nCause:\n{}').format(info, traceback.format_exc())
		sendToBot(s, msg)
	finally:
		s.logout()

def sellResources(s,e,fd):
	sys.stdin = os.fdopen(fd)
	try:
		banner()

		ciudades_comerciales = getCommertialCities(s)
		if len(ciudades_comerciales) == 0:
			print(_('There is no shop built'))
			enter()
			e.set()
			return

		if len(ciudades_comerciales) == 1:
			ciudad = ciudades_comerciales[0]
		else:
			ciudad = elegirCiudadComercial(ciudades_comerciales)
			banner()

		print(_('What resource do you want to sell?'))
		for indice, bien in enumerate(materials_names):
			print('({:d}) {}'.format(indice+1, bien))
		eleccion = read(min=1, max=len(materials_names))
		recurso = eleccion - 1
		banner()

		print(_('Do you want to sell to existing offers (1) or do you want to make your own offer (2)?'))
		rta = read(min=1, max=2)
		[venderAOfertas, crearOferta][rta - 1](s, ciudad, recurso, e)
		e.set()
	except KeyboardInterrupt:
		e.set()
		return

def do_it1(s, porVender, ofertas, recurso, ciudad):
	for oferta in ofertas:
		city, user, cant, precio, dist, idDestino = oferta
		city = city.strip()
		quiereComprar = cant.replace(',', '').replace('.', '')
		quiereComprar = int(quiereComprar)
		while True:
			barcos_disponibles = waitForArrival(s)
			cant_venta = quiereComprar if quiereComprar < porVender else porVender
			barcos_necesarios = int(math.ceil((Decimal(cant_venta) / Decimal(500))))
			barcos_usados = barcos_disponibles if barcos_disponibles < barcos_necesarios else barcos_necesarios
			if barcos_necesarios > barcos_usados:
				cant_venta = barcos_usados * 500
			porVender -= cant_venta
			quiereComprar -= cant_venta

			data = {'action': 'transportOperations', 'function': 'sellGoodsAtAnotherBranchOffice', 'cityId': ciudad['id'], 'destinationCityId': idDestino, 'oldView': 'branchOffice', 'position': ciudad['pos'], 'avatar2Name': user, 'city2Name': city, 'type': '333', 'activeTab': 'bargain', 'transportDisplayPrice': '0', 'premiumTransporter': '0', 'capacity': '5', 'max_capacity': '5', 'jetPropulsion': '0', 'transporters': str(barcos_usados), 'backgroundView': 'city', 'currentCityId': ciudad['id'], 'templateView': 'takeOffer', 'currentTab': 'bargain', 'actionRequest': 'REQUESTID', 'ajax': '1'}
			if recurso == 0:
				data['cargo_resource'] = str(cant_venta)
				data['resourcePrice'] = str(precio)
			else:
				data['tradegood{:d}Price'.format(recurso)] = str(precio)
				data['cargo_tradegood{:d}'.format(recurso)] = str(cant_venta)
			s.get('view=city&cityId={}'.format(ciudad['id']), noIndex=True)
			s.post(payloadPost=data)

			if porVender == 0:
				return
			if quiereComprar == 0:
				break

def do_it2(s, porVender, precio, recurso, cap_venta, ciudad):
	total = porVender
	html = getStoreInfo(s, ciudad)
	enVenta_inicial = vendiendo(html)[recurso]
	while True:
		html = getStoreInfo(s, ciudad)
		enVenta = vendiendo(html)[recurso]
		if enVenta < getstorageCapacityDeVenta(html):
			espacio = cap_venta - enVenta
			ofertar = porVender if espacio > porVender else espacio
			porVender -= ofertar
			nuevaVenta = enVenta + ofertar

			payloadPost = {'cityId': ciudad['id'], 'position': ciudad['pos'], 'action': 'CityScreen', 'function': 'updateOffers', 'resourceTradeType': '444', 'resource': '0', 'resourcePrice': '10', 'tradegood1TradeType': '444', 'tradegood1': '0', 'tradegood1Price': '11', 'tradegood2TradeType': '444', 'tradegood2': '0', 'tradegood2Price': '12', 'tradegood3TradeType': '444', 'tradegood3': '0', 'tradegood3Price': '17', 'tradegood4TradeType': '444', 'tradegood4': '0', 'tradegood4Price': '5', 'backgroundView': 'city', 'currentCityId': ciudad['id'], 'templateView': 'branchOfficeOwnOffers', 'currentTab': 'tab_branchOfficeOwnOffers', 'actionRequest': 'REQUESTID', 'ajax': '1'}
			if recurso == 0:
				payloadPost['resource'] = str(nuevaVenta)
				payloadPost['resourcePrice'] = str(precio)
			else:
				payloadPost['tradegood{:d}'.format(recurso)] = str(nuevaVenta)
				payloadPost['tradegood{:d}Price'.format(recurso)] = str(precio)
			s.post(payloadPost=payloadPost)

			if porVender == 0:
				break
		time.sleep(60 * 60 *  2)

	while True:
		html = getStoreInfo(s, ciudad)
		enVenta = vendiendo(html)[recurso]
		if enVenta <= enVenta_inicial:
			msg = _('{} of {} was sold at {:d}').format(addDot(total), materials_names[recurso], precio)
			sendToBot(s, msg)
			return
		time.sleep(60 * 60 *  2)
