#!/usr/bin/env python3

from datetime import date, datetime
from typing import NamedTuple
import requests
from requests.exceptions import HTTPError

from exceptions import *
from listener import Listener

import time
import json

#host = "192.168.0.20"
host = "localhost"; port = "8080"

class TAccess():
    def __init__(self, date0, date1, fac_id):
        self.jump = 8
        self.offset = 0
        self.date0 = date0
        self.date1 = date1
        self.fac_id = fac_id
        self.has_next:bool = None

    def next(self):
        try:
            r = requests.get("http://"+host+":"+port+"/api/rest/facility_access_log/"+int.__str__(self.fac_id).replace("'","")+"/"+
                    "daterange"+
                    "?offset=" + int.__str__(self.offset)+
                    "&limit=" + int.__str__(self.jump),
                headers={"x-hasura-admin-secret":"myadminsecretkey"},
                json={"startdate": "\""+self.date0+"\"", "enddate": "\""+self.date1+"\""})
            data = r.json()
            print("TAccess: next\n");print(data)
            if(data['access_log'] == []):
                raise TNoMoreAccesses
            self.offset += self.jump
            result = []
            length = data['access_log'].__len__()
            if(length <= (self.jump - 1)):
                self.has_next = False
            else:
                self.has_next = True
            for i in range(min(length, 7)):
                result.append( 
                    (data['access_log'][i]['user']['name']
                    ,data['access_log'][i]['user']['surname']
                    ,data['access_log'][i]['user']['email']
                    ,data['access_log'][i]['user']['phone']
                    ,data['access_log'][i]['user']['is_vaccinated']
                    ,self.fac_id))
            return result
        except KeyError:
            raise TrackingError
        except HTTPError as err: # El server no devuelve datos
            raise err

    def previous(self):
        try:
            if(self.offset < 0):
                raise TNoBeforeAccesses
            else:
                if(self.offset<self.jump):
                    self.offset = 0
                else:
                    self.offset -= self.jump
                r = requests.get("http://"+host+":"+port+"/api/rest/facility_access_log/"+int.__str__(self.fac_id).replace("'","")+"/"+
                    "daterange"+
                    "?offset=" + int.__str__(self.offset)+
                    "&limit=" + int.__str__(self.jump),
                    headers={"x-hasura-admin-secret":"myadminsecretkey"},
                    json={"startdate": "\""+self.date0+"\"", "enddate": "\""+self.date1+"\""})
                data = r.json()

                print("TAccess: previous\n");print(data)
                result = []
                if(data['access_log']==[]):
                    raise TNoBeforeAccesses
                for i in range(data['access_log'].__len__()):
                    result.append( 
                        (data['access_log'][i]['user']['name']
                        ,data['access_log'][i]['user']['surname']
                        ,data['access_log'][i]['user']['email']
                        ,data['access_log'][i]['user']['phone']
                        ,data['access_log'][i]['user']['is_vaccinated']
                        ,self.fac_id))
                return result
        except KeyError:
            raise TrackingError
        except HTTPError as err: # El server no devuelve datos
            if(self.offset != 0):
                self.offset -= self.jump
    
    # we only need one more access to confirm that there is a bunch more of accesses
    def isNext(self):
        if(self.has_next is not None):
            return self.has_next
        try:
            r = requests.get("http://"+host+":"+port+"/api/rest/facility_access_log/"+int.__str__(self.fac_id).replace("'","")+"/"+
                    "daterange"+
                    "?offset=" + int.__str__(self.offset)+
                    "&limit=" + int.__str__(1),
                headers={"x-hasura-admin-secret":"myadminsecretkey"},
                json={"startdate": "\""+self.date0+"\"", "enddate": "\""+self.date1+"\""})
            data = r.json()
            print("TAccess: next\n");print(data)
            if(data['access_log'] == []):
                return False
            return True
        except KeyError:
            raise RuntimeError
        except HTTPError as err: # El server no devuelve datos
            raise err


class UAccess():
    def __init__(self, date0, date1, userId):
        self.first_try = True
        self.jump = 2 + 1
        self.offset = 0
        self.date0 = date0
        self.date1 = date1
        self.userId = userId
        self.has_next = None

    def next(self):
        try:
            if(not self.first_try):
                self.offset += self.jump
            else:
                self.first_try = False

            r = requests.get("http://"+host+":"+port+"/api/rest/user_access_log/"+int.__str__(self.userId).replace("'","")+"/"+
                    "daterange"+
                    "?offset=" + int.__str__(self.offset)+
                    "&limit=" + int.__str__(self.jump),
                headers={"x-hasura-admin-secret":"myadminsecretkey"},
                json={"startdate": "\""+self.date0+"\"", "enddate": "\""+self.date1+"\""})
            data = r.json()
            print(data)
            if(data['access_log'] == []):
                raise UNoMoreAccesses
            if(data['access_log'].__len__() < 2):
                raise TrackingError
            if(data['access_log'].__len__() < 3):
                self.has_next = False
            else:
                self.has_next = True
            aux = data['access_log']
            return ((aux[0]['timestamp'], aux[0]['facility']['id']), (aux[1]['timestamp'], aux[1]['facility']['id']))
        except KeyError:
            raise TrackingError
        except HTTPError as err: # El server no devuelve datos
            if(self.offset != 0):
                self.offset -= self.jump
            raise err

    def previous(self):
        try:
            if(self.offset > 0):
                if(self.offset<self.jump):
                    self.offset = 0
                else:
                    self.offset -= self.jump
                
                r = requests.get("http://"+host+":"+port+"/api/rest/user_access_log/"+int.__str__(self.userId).replace("'","")+"/"+
                    "daterange"+
                    "?offset=" + int.__str__(self.offset)+
                    "&limit=" + int.__str__(self.jump),
                    headers={"x-hasura-admin-secret":"myadminsecretkey"},
                    json={"startdate": "\""+self.date0+"\"", "enddate": "\""+self.date1+"\""})
                data = r.json()
                if(data['access_log'] == []):
                    raise UNoBeforeAccesses
                if(data['access_log'].__len__() < 2):
                    raise TrackingError
                aux = data['access_log']
                return ((aux[0]['timestamp'], aux[0]['facility']['id']), (aux[1]['timestamp'], aux[1]['facility']['id']))
            else:
                raise UNoBeforeAccesses
        except KeyError:
            raise TrackingError
        except HTTPError as err: # El server no devuelve datos
            if(self.offset != 0):
                self.offset += self.jump
            raise err

    def reset(self):
        self.first_try = True
        self.offset = 0
    
    def hasNext(self):
        if(self.has_next is not None):
            return self.has_next
        try:
            r = requests.get("http://"+host+":"+port+"/api/rest/user_access_log/"+int.__str__(self.userId).replace("'","")+"/"+
                "daterange"+
                "?offset=" + int.__str__(self.offset)+
                "&limit=" + int.__str__(1),
                headers={"x-hasura-admin-secret":"myadminsecretkey"},
                json={"startdate": "\""+self.date0+"\"", "enddate": "\""+self.date1+"\""})
            data = r.json()
            if(data['access_log'] == []):
                return False
            return True
        except KeyError:
            raise RuntimeError
        except HTTPError as err: # El server no devuelve datos
            raise err


class CAccess():
    def __init__(self, date0, date1, userId):
        print("Creating CAccess instance with values:\n"
            +date0+"\n"
            +date1+"\n"
            +userId)
        self.u_accesses = UAccess(date0, date1, userId)
        self.t_accesses = None
    
    def next(self):
        try:
            if(self.t_accesses is None):
                (date0, id_0), (date1, _) = self.u_accesses.next()
                self.t_accesses = TAccess(date0, date1, id_0)
            results = self.t_accesses.next()
            return results
        except UNoMoreAccesses:
            raise NoMoreAccesses
        except TNoMoreAccesses:
            del self.t_accesses
            self.t_accesses = None
            return self.next()
        except KeyError:
            raise TrackingError

    def previous(self):
        try:
            if(self.t_accesses is None):
                (date0, id_0), (date1, _) = self.u_accesses.previous()
                self.t_accesses = TAccess(date0, date1, id_0)
                results = self.t_accesses.next()
            results = self.t_accesses.previous()
            return results
        except UNoBeforeAccesses:
            raise NoBeforeAccesses
        except TNoBeforeAccesses:
            del self.t_accesses
            self.t_accesses = None
        except KeyError:
            raise TrackingError
        
    def reset(self):
        try:
            del self.t_accesses
            self.t_accesses = None
            self.u_accesses.reset()
            (date0, id_0), (date1, _) = self.u_accesses.next()
            self.t_accesses = TAccess(date0, date1, id_0)
            return self.t_accesses.next()
        except UNoMoreAccesses:
            raise NoMoreAccesses
        except TNoMoreAccesses:
            del self.t_accesses
            self.t_accesses = None
        except KeyError:
            raise TrackingError
    
    def hasNext(self):
        if(self.t_accesses is None):
            return self.u_accesses.hasNext()
        return (self.u_accesses.hasNext() or self.t_accesses.isNext())


class Facility:
    def __init__(self, name, address, id):
        self.name = name
        self.address = address
        self.id = id


class Access:
    def __init__(self, data):
        self.time = data["timestamp"]
        self.temp = data["temperature"]
        self.type = data["type"]
        self.facility = Facility(data["facility"]["name"], data["facility"]["address"], data["facility"]["id"])
    
    def setAccess(self, data):
        self.time = data["timestamp"]
        self.temp = data["temperature"]
        self.type = data["type"]
        self.facility = Facility(data["facility"]["name"], data["facility"]["address"], data["facility"]["id"])
    
    def tupleAccess(self):
        return (self.time, self.temp, self.type, self.facility.name, self.facility.address, self.facility.id)


class Accesses:
    def __init__(self, userId):
        self.userId = userId
        self.offset = 0
        self.jump = 8
        self.last_trunk = False
    
    def hasNext(self):
        return (not self.last_trunk)

    def next(self):
        #Debugging info
        print("Accesses.next():"+"\n\t"
            +"offset: "+int.__str__(self.offset)+"\n"
            +"\tlast_trunk: "+bool.__str__(self.last_trunk))
        
        if(self.last_trunk != True):    
            self.offset += self.jump
        else:
            raise NoMoreAccesses
    
    def hasPrev(self):
        return (self.offset == 0)

    def prev(self):
        #Debugging info
        print("Accesses.prev():"+"\n\t"
            +"offset: "+int.__str__(self.offset)+"\n"
            +"\tlast_trunk: "+bool.__str__(self.last_trunk))
        
        if(self.offset == 0):
            raise NoMoreAccesses
        if(self.offset < self.jump):
            self.offset = 0
            raise NoMoreAccesses
        elif(self.last_trunk):
            self.last_trunk = False
            self.offset -= self.jump
        else:
            self.offset -= self.jump

    def getAccesses(self):
        #debugging info
        print("getAccesses method:\n\t"+
            "offset: "+int.__str__(self.offset)+"\n\t"+
            "jump: "+int.__str__(self.jump))
        
        try:
            r = requests.get("http://"+host+":"+port+"/api/rest/user_access_log/"+int.__str__(self.userId).replace("'","")
                +"?offset=" + int.__str__(self.offset)+
                "&limit=" + int.__str__(self.jump),
            headers={"x-hasura-admin-secret":"myadminsecretkey"})
            data = r.json()
            last_accesses = False, (self.offset == 0)
            access = []
            if(data['access_log']!=[]):
                length = data['access_log'].__len__()
                for i in range(min(length, 7)):
                    access.insert(access.__len__(), Access(data['access_log'][i]))
                if(length <= (self.jump - 1)):
                    print("Length of accesses list: ", int.__str__(length))
                    last_accesses = True, (self.offset == 0)
                    self.last_trunk = True
            else:
                last_accesses = True, (self.offset == 0)
            print(access)
        finally:
            return access, last_accesses


    def accessesToList(accesses):
        list = []
        for a in accesses:
            list.append(a.tupleAccess())
        return list

    def getAccessesFacility(self):
        r = requests.get("http://"+host+":"+port+"/api/rest/facility_access_log/"+self.id,
        headers={"x-hasura-admin-secret":"myadminsecretkey"})


class PersonData:
    def __init(self):
        self.username = None
        self.password = None
        self.email = None
        self.phone = None
        self.is_vaccinated = None
        self.name = None
        self.surname = None
        self.uuid = None
        self.accesses:Accesses = None
        self.tracking:CAccess = None

    def qr(self):
        self.name, self.surname, self.uuid

    def addUser(self):
        r = requests.post("http://"+host+":"+port+"/api/rest/user",
        headers={"x-hasura-admin-secret":"myadminsecretkey"},
        data={
            "username": self.username, 
            "password" : self.password,
            "email" : self.email,
            "phone" : self.phone,
            "is_vaccinated" : self.is_vaccinated,
            "name" : self.name,
            "surname" : self.surname,
            "uuid" : self.uuid})

    def readUser(self):
        r = requests.post("http://"+host+":"+port+"/api/rest/login?username="+self.username+"&password="+self.password,
        headers={"x-hasura-admin-secret":"myadminsecretkey"})
        data = json.loads(r)
        self.username      = data['username']
        self.password      = data['password']
        self.email         = data['email']
        self.phone         = data['phone']
        self.is_vaccinated = data['is_vaccinated']
        self.name          = data['name']
        self.surname       = data['surname']
        self.uuid          = data['uuid']

    ## CU-01 related: Search user by fields
    def searchUser(self, name, surname):
        print("Searching for user: "+name+" "+surname)
        try:
            time.sleep(4)
            r = requests.get("http://"+host+":"+port+"/api/rest/user?name="+name+"&surname="+surname,
            headers={"x-hasura-admin-secret":"myadminsecretkey"})
            data = r.json()
            print(data)
            if(data['users']!=[]):
                self.email         = data['users'][0]['email']
                self.phone         = data['users'][0]['phone']
                self.is_vaccinated = data['users'][0]['is_vaccinated']
                self.name          = data['users'][0]['name']
                self.surname       = data['users'][0]['surname']
                self.uuid          = data['users'][0]['uuid']
                self.accesses      = Accesses(self.uuid)
                print("User has been found")
                return 1
            print("User has not been found")
            raise UserNotFound
        except HTTPError:
            print("HTTP Error, no connection with DB")
            raise HTTPError

    ## CU-02 related: Tracking methods
    def track(self, t0, t1):
        self.tracking = CAccess(t0, t1, self.uuid)
    
    def track_next(self):
        try:
            aux = self.tracking.next(); print(aux)
            return aux
        except NoMoreAccesses:
            raise NoMoreAccesses
    
    def track_hasNext(self):
        return self.tracking.hasNext()
        
    def track_previous(self):
        try:
            return self.tracking.previous()
        except NoBeforeAccesses:
            raise NoBeforeAccesses
    
    def track_reset(self):
        try:
            return self.tracking.reset()
        except NoMoreAccesses:
            raise NoMoreAccesses


class WatcherData:
    def __init__(self):
        self.search_name = ""
        self.search_surname = ""
        self.dataUser = PersonData()
        self.since: date = datetime(year= 1995, month= 10, day= 20)
        self.s_time = 0,0
        self.until: date = datetime(year= 2995, month= 10, day= 20)
        self.u_time = 0,0
        self.listeners:list(Listener) = []
        self.is_searching = False

    def insertListener(self, listener):
        print("New listener on town")
        self.listeners.insert(self.listeners.__len__(), listener)

    def reset(self):
        self.search_name = ""
        self.search_surname = ""

    def search(self):
        #triming spaces from name
        self.search_name = self.search_name.strip() #replace(" ", "", -1)
        #triming spaces from surname
        self.search_surname = self.search_surname.strip()
        if(self.dataUser.searchUser(self.search_name, self.search_surname) == 1): #"Rosa", "Melano")
            print("Iterating listener's list :")
            print([])
            print(self.listeners)
            for listener in self.listeners:
                listener.action(Listener.s_u_event)
        else:
            #error in search
            raise UserNotFound()

    def track(self):
        try:
            self.is_searching = True                #Search has started
            #self.dataUsers = self.dataUser.track(self.since, self.until)
            date0 = int.__str__(self.since.year) + "-" + int.__str__(self.since.month) + "-" +  int.__str__(self.since.day) + "T" + int.__str__(self.s_time[0]) + ":" + int.__str__(self.s_time[1]) + ":" + "00.000000+00:00"
            date1 = int.__str__(self.until.year) + "-" +  int.__str__(self.until.month) + "-" +  int.__str__(self.until.day) + "T"  + int.__str__(self.u_time[0]) + ":" + int.__str__(self.u_time[1]) + ":" + "00.000000+00:00"
            self.dataUsers = self.dataUser.track(date0, date1)
            self.is_searching = False               #Search has been finished
            for listener in self.listeners:
                listener.action(Listener.track_event)
        except Exception:
            #error tracking
            self.is_searching = False               #Search has been finished
            raise TrackingError()   

    def track_next(self):
        return self.dataUser.track_next()

    def track_previous(self):
        return self.dataUser.track_previous()

    def track_reset(self):
        return self.dataUser.track_reset()
    
    def track_hasNext(self):
        return self.dataUser.track_hasNext()

    def valid_time(self):
        if(self.s_time[0] == None or self.s_time[1] == None or self.u_time[0] == None or self.u_time[1] == None):
            return False
        else:
            return True

    def is_valid(self):
        error = (self.search_name is None or self.search_surname is None)
        error = error or (self.search_name == "" or self.search_surname == "")
        print("data is "+(lambda boolean: "True" if boolean else "False") (not error))
        return not error
    
    def valid_dates(self):
        error_1 = (self.since is None or self.s_time[0] is None or self.s_time[1] is None)
        error_1 = error_1 or self.s_time[0] > 23 or self.s_time[0] < 0 or self.s_time[1] > 59 or self.s_time[1] < 0
        print("Since date is "+(lambda boolean: "True" if boolean else "False") (not error_1))

        error_2 = (self.until is None or self.u_time[0] is None or self.u_time[1] is None)
        error_2 = error_2 or self.u_time[0] > 23 or self.u_time[0] < 0 or self.u_time[1] > 59 or self.u_time[1] < 0
        print("Until date is "+(lambda boolean: "True" if boolean else "False") (not error_2))
        return (not error_1, not error_2)
