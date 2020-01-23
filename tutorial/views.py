# Copyright (c) Microsoft. All rights reserved. Licensed under the MIT license. See LICENSE.txt in the project root for license information.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from tutorial.authhelper import get_signin_url, get_token_from_code, get_access_token
from tutorial.outlookservice import get_me, get_my_messages, get_my_events, get_my_contacts, get_my_feeds
import time

# Create your views here.

def home(request):
  redirect_uri = request.build_absolute_uri(reverse('tutorial:gettoken'))
  sign_in_url = get_signin_url(redirect_uri)
  context = { 'signin_url': sign_in_url }
  return render(request, 'tutorial/home.html', context)

def gettoken(request):
  auth_code = request.GET['code']
  redirect_uri = request.build_absolute_uri(reverse('tutorial:gettoken'))
  token = get_token_from_code(auth_code, redirect_uri)
  access_token = token['access_token']
  user = get_me(access_token)
  refresh_token = token['refresh_token']
  expires_in = token['expires_in']

  # expires_in is in seconds
  # Get current timestamp (seconds since Unix Epoch) and
  # add expires_in to get expiration time
  # Subtract 5 minutes to allow for clock differences
  expiration = int(time.time()) + expires_in - 300

  # Save the token in the session
  request.session['access_token'] = access_token
  request.session['refresh_token'] = refresh_token
  request.session['token_expires'] = expiration
  print('Himanshu adding line below to print th token')
  print(HttpResponse.content)
  return HttpResponseRedirect(reverse('tutorial:mail'))

def mail(request):
  access_token = get_access_token(request, request.build_absolute_uri(reverse('tutorial:gettoken')))
  # If there is no token in the session, redirect to home
  if not access_token:
    return HttpResponseRedirect(reverse('tutorial:home'))
  else:
    messages = get_my_messages(access_token)
    context = { 'messages': messages['value'] }
    return render(request, 'tutorial/mail.html', context)

def events(request):
  access_token = get_access_token(request, request.build_absolute_uri(reverse('tutorial:gettoken')))
  # If there is no token in the session, redirect to home
  if not access_token:
    return HttpResponseRedirect(reverse('tutorial:home'))
  else:
    events = get_my_events(access_token)
    context = { 'events': events['value'] }
    return render(request, 'tutorial/events.html', context)

def contacts(request):
  access_token = get_access_token(request, request.build_absolute_uri(reverse('tutorial:gettoken')))
  # If there is no token in the session, redirect to home
  if not access_token:
    res =HttpResponseRedirect(reverse('tutorial:home'))
    print(res.content)
    return res
  else:
    contacts = get_my_contacts(access_token)
    context = { 'contacts': contacts['value'] }
    return render(request, 'tutorial/contacts.html', context)
  #######################################TEST STRTS FROM HERE ##############################
def contacts_org(request):
  access_token = get_access_token(request, request.build_absolute_uri(reverse('tutorial:gettoken')))
  # If there is no token in the session, redirect to home
  if not access_token:
    return HttpResponseRedirect(reverse('tutorial:home'))
  else:
    contacts = get_my_contacts(access_token)
    context = { 'contacts': contacts['value'] }
    return render(request, 'tutorial/contacts.html', context)

def feeds(request):
    access_token = get_access_token(request, request.build_absolute_uri(reverse('tutorial:gettoken')))
    #user_email = request.session['user_email']
    # If there is no token in the session, redirect to home
    if not access_token:
      return HttpResponseRedirect(reverse('tutorial:home'))
    else:
      feeds=get_my_feeds(access_token)
      print(feeds)
      #context = {'feeds': feeds['value'] }
      context = {'feeds': feeds['value']}
      print("-------BELOW IS FEED ------")
      print(feeds['value'])
      return render(request, 'tutorial/feeds.html', context)
    #GET https://manage.office.com/api/v1.0/41463f53-8812-40f4-890f-865bf6e35190/activity/feed/audit/301299007231$301299007231$41463f53881240f4890f865bf6e35190aad2015062920$e1c2ab19858a469fb1f1fd097effffc9$04 HTTP/1.1
    #Authorization: Bearer eyJ0e...Qa6wg