# -*- coding: utf-8 -*-
#
# Copyright © 2012 - 2013 Michal Čihař <mcihar@suse.cz>
#
# This file is part of python-suseapi <https://github.com/nijel/python-suseapi>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
'''
Support classes for caching data.
'''
from datetime import datetime, timedelta


class CacherMixin(object):
    '''
    Generic cacher mixin using object attribute.
    '''
    _cache = {}
    cache_key = 'cache-%s'

    def _cache_key(self, key):
        '''
        Get name of the cache key for django caching.
        '''
        return self.cache_key % key

    def _cache_set(self, key, value):
        '''
        Remembers value in internal cache.
        '''
        self._cache[self._cache_key(key)] = (value, datetime.now())

    def _cache_uptodate(self, key):
        '''
        Checks whether cache entry is valid.
        '''
        expires = self._cache[self._cache_key(key)][1] + timedelta(days=1)
        return expires > datetime.now()

    def _cache_get(self, key, force=False):
        '''
        Gets value from internal cache.
        '''
        if (self._cache_key(key) in self._cache
                and (force or self._cache_uptodate(key))):
            return self._cache[self._cache_key(key)][0]
        return None


class DjangoCacherMixin(CacherMixin):
    '''
    Cacher mixin using Django.
    '''

    def _cache_set(self, key, value):
        '''
        Sets value in django cache.
        '''
        from django.core.cache import cache
        cache.set(self._cache_key(key), value, 24 * 3600)

    def _cache_get(self, key, force=False):
        '''
        Gets value from django cache.
        '''
        from django.core.cache import cache
        return cache.get(self._cache_key(key))
