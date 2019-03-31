from application.TDG import ClinicTDG

# Returns clinic if found
def getClinic(id):
    clinic = ClinicTDG.find(id)
    if clinic is not None:
        return clinic
    return False

# Return all clinics
def getAllClinics():
    return ClinicTDG.findAll()

# check if clinic exists (only for creating data -- check if name and address exist in table already)
def clinicExists(name, address):
    clinic = ClinicTDG.findByData(name, address)
    if clinic is not None:
        return True
    return False

def clinicExists(id):
    clinic = ClinicTDG.find(id)
    if clinic is not None:
        return True
    return False

# create new clinic
def createClinic(name, address):
    reponse = False
    if (clinicExists(name, address)):
        response = False
    else:
        ClinicTDG.create(name, address)
        response = True
    return response

# delete a clinic
def deleteClinic(id):
    reponse = False
    if (getClinic(id) is None):
        response = False
    else:
        ClinicTDG.delete(id)
        response = True
    return response

def updateClinic(id, name, address):
    ClinicTDG.update(id, name, address)
    updatedClinic = ClinicTDG.getClinic(id)
    if ((updatedClinic.name == name) & (updatedClinic.address == address)):
        return True
    return False