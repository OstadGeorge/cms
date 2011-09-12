# -*- coding: utf-8 -*-

# Programming contest management system
# Copyright © 2011 Luca Wehrstedt <luca.wehrstedt@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pyjamas.ui.UIObject import UIObject

from pyjamas import Window
from pyjamas import DOM

from __pyjamas__ import JS


class TeamSearch(object):
    def __init__(self, ds):
        self.ds = ds

        inputfield = DOM.getElementById('team_search_input')
        background = DOM.getElementById('team_search_bg')

        JS('''
        inputfield.addEventListener("focus", function(evt){
            self.show();
        });

        inputfield.addEventListener("input", function(evt){
            self.update();
        });

        background.addEventListener("click", function(evt){
            if (evt.target == background){
                self.hide();
            }
        });
        ''')

        self.t_head = DOM.getElementById('team_search_head')
        self.t_body = DOM.getElementById('team_search_body')

        self.body = UIObject(Element=DOM.getElementById('body'))
        self.open = False

    def show(self):
        if not self.open:
            inner_html = ''
            for t_id, team in sorted(self.ds.teams.iteritems(), key=lambda a:a[1]['name']):
                # FIXME hardcoded flag path
                inner_html += '''
    <div class="item" id="''' + t_id + '''">
        <input type="checkbox" id="''' + t_id + '''_check" />
        <label for="''' + t_id + '''_check">
            <img class="flag" src="/flags/''' + t_id + '''.png" />
            ''' + team['name'] + '''
        </label>
    </div>'''
            DOM.setInnerHTML(self.t_body, inner_html)

            self.body.addStyleName('team_search')
            self.open = True

    def hide(self):
        if self.open:
            self.body.removeStyleName('team_search')
            self.open = False

    def update(self):
        inputfield = DOM.getElementById('team_search_input')
        search_text = DOM.getAttribute(inputfield, 'value')

        if search_text == '':
            for t_id, team in self.ds.teams.iteritems():
                el = UIObject(Element=DOM.getElementById(t_id))
                el.removeStyleName('hidden')
        else:
            for t_id, team in self.ds.teams.iteritems():
                if team['name'][0:len(search_text)] == search_text:
                    el = UIObject(Element=DOM.getElementById(t_id))
                    el.removeStyleName('hidden')
                else:
                    el = UIObject(Element=DOM.getElementById(t_id))
                    el.addStyleName('hidden')

