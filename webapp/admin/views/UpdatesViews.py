# Copyright 2017 the Isard-vdi project authors:
#      Josep Maria Viñolas Auquer
#      Alberto Larraz Dalmases
# License: AGPLv3

#!flask/bin/python
# coding=utf-8
import json

from flask import render_template, Response, request, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user

from webapp import app
from ...lib import admin_api

app.adminapi = admin_api.isardAdmin()

from ...lib.isardUpdates import Updates
u=Updates()

from .decorators import isAdmin

@app.route('/admin/updates', methods=['GET'])
@login_required
@isAdmin
def admin_updates():
    registered=u.is_registered()
    if not registered:
        flash("Unable to contact updates website.","error")
    return render_template('admin/pages/updates.html', nav="Updates", registered=registered)

@app.route('/admin/updates_register', methods=['POST'])
@login_required
@isAdmin
def admin_updates_register():
    if request.method == 'POST':
        try:
            if not u.is_registered():
                u.register()
        except Exception as e:
            log.error('Error registering client: '+str(e))
            #~ return False
    return redirect(url_for('admin_updates'))
            
@app.route('/admin/updates/<kind>', methods=['GET'])
@login_required
@isAdmin
def admin_updates_json(kind):
        try:
            return json.dumps(u.getNewKind(kind,current_user.id))
        except Exception as e:
            print('exception on read updates: '+str(e))
            return json.dumps([])

@app.route('/admin/updates/update/<kind>', methods=['POST'])
@app.route('/admin/updates/update/<kind>/<id>', methods=['POST'])
@login_required
@isAdmin
def admin_updates_update(kind,id=False):
    if request.method == 'POST':
        if id is not False:
            # Only one id
            d=u.getNewKindId(kind,current_user.id,id)
            if d is not False:
                if kind == 'domains':
                    d=u.formatDomains([d],current_user)[0]
                elif kind == 'media':
                    d=u.formatMedias([d],current_user)[0]
                app.adminapi.insert_or_update_table_dict(kind,d)
        else:
            # No id, do it will all
            data=u.getNewKind(kind,current_user.id)
            data=[d for d in data if d['new'] is True]
            if kind == 'domains': 
                data=u.formatDomains(data,current_user)
            elif kind == 'media':
                data=u.formatMedias(data,current_user)
        app.adminapi.insert_or_update_table_dict(kind,data)
    return json.dumps([])


    
