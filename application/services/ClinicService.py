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

# create new clinic
def createClinic(name, address):
    reponse = False
    if (clinicExists(name, address)):
        response = False
    else:
        ClinicTDG.create(name, address)
        response = True
    return response