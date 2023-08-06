#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import math
import json
import gettext
import traceback
from decimal import *
from ikabot.helpers.process import set_child_mode
from ikabot.helpers.varios import addDot
from ikabot.helpers.gui import enter, banner
from ikabot.helpers.getJson import getCiudad
from ikabot.helpers.signals import setInfoSignal
from ikabot.helpers.planearViajes import waitForArrival
from ikabot.helpers.pedirInfo import getIdsOfCities, read
from ikabot.config import *
from ikabot.helpers.botComm import *
from ikabot.helpers.recursos import *
from ikabot.helpers.tienda import *

t = gettext.translation('buyResources', 
                        localedir, 
                        languages=idiomas,
                        fallback=True)
_ = t.gettext

def asignarRecursoBuscado(s, ciudad):
	print(_('Which resource do you want to buy?'))
	for indice, bien in enumerate(materials_names):
		print('({:d}) {}'.format(indice+1, bien))
	eleccion = read(min=1, max=5)
	recurso = eleccion - 1
	if recurso == 0:
		recurso = 'resource'
	data = {
	'cityId': ciudad['id'],
	'position': ciudad['pos'],
	'view': 'branchOffice',
	'activeTab': 'bargain',
	'type': 444,
	'searchResource': recurso,
	'range': ciudad['rango'],
	'backgroundView' : 'city',
	'currentCityId': ciudad['id'],
	'templateView': 'branchOffice',
	'currentTab': 'bargain',
	'actionRequest': s.token(),
	'ajax': 1
	}
	rta = s.post(payloadPost=data)
	return eleccion, recurso

def obtenerOfertas(s, ciudad):
	html = getStoreHtml(s, ciudad)
	hits = re.findall(r'short_text80">(.*?) *<br/>\((.*?)\)\s *</td>\s *<td>(\d+)</td>\s *<td>(.*?)/td>\s *<td><img src="skin/resources/icon_(\w+)\.png[\s\S]*?white-space:nowrap;">(\d+)\s[\s\S]*?href="\?view=takeOffer&destinationCityId=(\d+)&oldView=branchOffice&activeTab=bargain&cityId=(\d+)&position=(\d+)&type=(\d+)&resource=(\w+)"', html)
	ofertas = []
	for hit in hits:
		oferta = {
		'ciudadDestino': hit[0],
		'jugadorAComprar' : hit[1],
		'bienesXminuto': int(hit[2]),
		'cantidadDisponible': int(hit[3].replace(',', '').replace('.', '').replace('<', '')),
		'tipo': hit[4],
		'precio': int(hit[5]),
		'destinationCityId': hit[6],
		'cityId': hit[7],
		'position': hit[8],
		'type': hit[9],
		'resource': hit[10]
		}
		ofertas.append(oferta)
	return ofertas

def calcularCosto(ofertas, cantidadAComprar):
	costoTotal = 0
	for oferta in ofertas:
		if cantidadAComprar == 0:
			break
		comprar = oferta['cantidadDisponible'] if oferta['cantidadDisponible'] < cantidadAComprar else cantidadAComprar
		cantidadAComprar -= comprar
		costoTotal += comprar * oferta['precio']
	return costoTotal

def getOro(s, ciudad):
	url = 'view=finances&backgroundView=city&currentCityId={}&templateView=finances&actionRequest={}&ajax=1'.format(ciudad['id'], s.token())
	data = s.post(url)
	json_data = json.loads(data, strict=False)
	oro = json_data[0][1]['headerData']['gold']
	return int(oro.split('.')[0])

def elegirCiudadComercial(ciudades_comerciales):
	print(_('From which city do you want to buy resources?\n'))
	for i, ciudad in enumerate(ciudades_comerciales):
		print('({:d}) {}'.format(i + 1, ciudad['name']))
	ind = read(min=1, max=len(ciudades_comerciales))
	return ciudades_comerciales[ind - 1]

def buyResources(s,e,fd):
	sys.stdin = os.fdopen(fd)
	try:
		banner()

		ciudades_comerciales = getCiudadesComerciales(s)
		if len(ciudades_comerciales) == 0:
			print(_('There is no store build'))
			enter()
			e.set()
			return

		if len(ciudades_comerciales) == 1:
			ciudad = ciudades_comerciales[0]
		else:
			ciudad = elegirCiudadComercial(ciudades_comerciales)
			banner()

		numRecurso, recurso = asignarRecursoBuscado(s, ciudad)
		banner()

		ofertas = obtenerOfertas(s, ciudad)
		if len(ofertas) == 0:
			print(_('There were no offers found.'))
			e.set()
			return

		precio_total   = 0
		cantidad_total = 0
		for oferta in ofertas:
			cantidad = oferta['cantidadDisponible']
			unidad   = oferta['precio']
			costo    = cantidad * unidad
			print(_('amount:{}').format(addDot(cantidad)))
			print(_('price :{:d}').format(unidad))
			print(_('cost  :{}').format(addDot(costo)))
			print('')
			precio_total += costo
			cantidad_total += cantidad

		disponible = ciudad['freeSpaceForResources'][numRecurso - 1]

		print(_('Total amount available to purchase: {}, for {}').format(addDot(cantidad_total), addDot(precio_total)))
		if disponible < cantidad_total:
			print(_('You just can buy {} due to storing capacity').format(addDot(disponible)))
			cantidad_total = disponible
		print('')
		cantidadAComprar = read(msg=_('How much do you want to buy?: '), min=0, max=cantidad_total)
		if cantidadAComprar == 0:
			e.set()
			return

		oro = getOro(s, ciudad)
		costoTotal = calcularCosto(ofertas, cantidadAComprar)

		print(_('\nCurrent gold: {}.\nTotal cost  : {}.\nFinal gold  : {}.'). format(addDot(oro), addDot(costoTotal), addDot(oro - costoTotal)))
		print(_('Proceed? [Y/n]'))
		rta = read(values=['y', 'Y', 'n', 'N', ''])
		if rta.lower() == 'n':
			e.set()
			return

		print(_('It will be purchased {}').format(addDot(cantidadAComprar)))
		enter()
	except KeyboardInterrupt:
		e.set()
		return

	set_child_mode(s)
	e.set()

	info = _('\nI will buy {} from {} to {}\n').format(addDot(cantidadAComprar), materials_names[numRecurso - 1], ciudad['cityName'])
	setInfoSignal(s, info)
	try:
		do_it(s, ciudad, ofertas, cantidadAComprar)
	except:
		msg = _('Error in:\n{}\nCause:\n{}').format(info, traceback.format_exc())
		sendToBot(s, msg)
	finally:
		s.logout()

def buy(s, ciudad, oferta, cantidad):
	barcos = int(math.ceil((Decimal(cantidad) / Decimal(500))))
	data_dict = {
	'action': 'transportOperations',
	'function': 'buyGoodsAtAnotherBranchOffice',
	'cityId': oferta['cityId'],
	'destinationCityId': oferta['destinationCityId'],
	'oldView': 'branchOffice',
	'position': ciudad['pos'],
	'avatar2Name': oferta['jugadorAComprar'],
	'city2Name': oferta['ciudadDestino'],
	'type': int(oferta['type']),
	'activeTab': 'bargain',
	'transportDisplayPrice': 0,
	'premiumTransporter': 0,
	'capacity': 5,
	'max_capacity': 5,
	'jetPropulsion': 0,
	'transporters': barcos,
	'backgroundView': 'city',
	'currentCityId': oferta['cityId'],
	'templateView': 'takeOffer',
	'currentTab': 'bargain',
	'actionRequest': s.token(),
	'ajax': 1
	}
	url = 'view=takeOffer&destinationCityId={}&oldView=branchOffice&activeTab=bargain&cityId={}&position={}&type={}&resource={}&backgroundView=city&currentCityId={}&templateView=branchOffice&actionRequest={}&ajax=1'.format(oferta['destinationCityId'], oferta['cityId'], oferta['position'], oferta['type'], oferta['resource'], oferta['cityId'], s.token())
	data = s.post(url)
	html = json.loads(data, strict=False)[1][1][1]
	hits = re.findall(r'"tradegood(\d)Price"\s*value="(\d+)', html)
	for hit in hits:
		data_dict['tradegood{}Price'.format(hit[0])] = int(hit[1])
		data_dict['cargo_tradegood{}'.format(hit[0])] = 0
	hit = re.search(r'"resourcePrice"\s*value="(\d+)', html)
	if hit:
		data_dict['resourcePrice'] = int(hit.group(1))
		data_dict['cargo_resource'] = 0
	resource = oferta['resource']
	if resource == 'resource':
		data_dict['cargo_resource'] = cantidad
	else:
		data_dict['cargo_tradegood{}'.format(resource)] = cantidad
	s.post(payloadPost=data_dict)
	msg = _('I buy {} to {} from {}').format(addDot(cantidad), oferta['ciudadDestino'], oferta['jugadorAComprar'])
	sendToBotDebug(s, msg, debugON_buyResources)

def do_it(s, ciudad, ofertas, cantidadAComprar):
	while True:
		for oferta in ofertas:
			if cantidadAComprar == 0:
				return
			if oferta['cantidadDisponible'] == 0:
				continue
			barcosDisp = waitForArrival(s)
			storageCapacity  = barcosDisp * 500
			comprable_max = storageCapacity if storageCapacity < cantidadAComprar else cantidadAComprar
			compra = comprable_max if oferta['cantidadDisponible'] > comprable_max else oferta['cantidadDisponible']
			cantidadAComprar -= compra
			oferta['cantidadDisponible'] -= compra
			buy(s, ciudad, oferta, compra)
			break # vuelvo a empezar desde el principio
