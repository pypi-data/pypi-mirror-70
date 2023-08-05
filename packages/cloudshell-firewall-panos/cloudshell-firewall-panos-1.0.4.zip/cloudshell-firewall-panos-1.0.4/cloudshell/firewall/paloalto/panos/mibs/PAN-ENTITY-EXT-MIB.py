#
# PySNMP MIB module PAN-ENTITY-EXT-MIB (http://pysnmp.sf.net)
# ASN.1 source http://mibs.snmplabs.com:80/asn1/PAN-ENTITY-EXT-MIB
# Produced by pysmi-0.2.2 at Wed Oct 03 13:14:04 2018
# On host ? platform ? version ? by user ?
# Using Python version 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
#
Integer, ObjectIdentifier, OctetString = mibBuilder.importSymbols("ASN1", "Integer", "ObjectIdentifier", "OctetString")
NamedValues, = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
ConstraintsUnion, SingleValueConstraint, ConstraintsIntersection, ValueSizeConstraint, ValueRangeConstraint = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsUnion", "SingleValueConstraint", "ConstraintsIntersection", "ValueSizeConstraint", "ValueRangeConstraint")
entPhysicalIndex, = mibBuilder.importSymbols("ENTITY-MIB", "entPhysicalIndex")
panModules, = mibBuilder.importSymbols("PAN-GLOBAL-REG", "panModules")
NotificationGroup, ModuleCompliance, ObjectGroup = mibBuilder.importSymbols("SNMPv2-CONF", "NotificationGroup", "ModuleCompliance", "ObjectGroup")
Integer32, MibScalar, MibTable, MibTableRow, MibTableColumn, NotificationType, MibIdentifier, IpAddress, TimeTicks, Counter64, Unsigned32, ModuleIdentity, Gauge32, iso, ObjectIdentity, Bits, Counter32 = mibBuilder.importSymbols("SNMPv2-SMI", "Integer32", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "NotificationType", "MibIdentifier", "IpAddress", "TimeTicks", "Counter64", "Unsigned32", "ModuleIdentity", "Gauge32", "iso", "ObjectIdentity", "Bits", "Counter32")
DisplayString, TextualConvention = mibBuilder.importSymbols("SNMPv2-TC", "DisplayString", "TextualConvention")
panEntityMIBModule = ModuleIdentity((1, 3, 6, 1, 4, 1, 25461, 1, 1, 7))
panEntityMIBModule.setRevisions(('2012-11-05 11:06',))
if mibBuilder.loadTexts: panEntityMIBModule.setLastUpdated('201211051106Z')
if mibBuilder.loadTexts: panEntityMIBModule.setOrganization('Palo Alto Networks')
panEntityMIBObjects = MibIdentifier((1, 3, 6, 1, 4, 1, 25461, 1, 1, 7, 1))
panEntityMIBConformance = MibIdentifier((1, 3, 6, 1, 4, 1, 25461, 1, 1, 7, 2))
panEntityChassisGroup = ObjectIdentity((1, 3, 6, 1, 4, 1, 25461, 1, 1, 7, 1, 1))
if mibBuilder.loadTexts: panEntityChassisGroup.setStatus('current')
panEntityFRUModuleGroup = ObjectIdentity((1, 3, 6, 1, 4, 1, 25461, 1, 1, 7, 1, 2))
if mibBuilder.loadTexts: panEntityFRUModuleGroup.setStatus('current')
panEntityFanTrayGroup = ObjectIdentity((1, 3, 6, 1, 4, 1, 25461, 1, 1, 7, 1, 3))
if mibBuilder.loadTexts: panEntityFanTrayGroup.setStatus('current')
panEntityPowerSupplyGroup = ObjectIdentity((1, 3, 6, 1, 4, 1, 25461, 1, 1, 7, 1, 4))
if mibBuilder.loadTexts: panEntityPowerSupplyGroup.setStatus('current')
panEntityTotalPowerAvail = MibScalar((1, 3, 6, 1, 4, 1, 25461, 1, 1, 7, 1, 1, 1), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: panEntityTotalPowerAvail.setStatus('current')
panEntityTotalPowerUsed = MibScalar((1, 3, 6, 1, 4, 1, 25461, 1, 1, 7, 1, 1, 2), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: panEntityTotalPowerUsed.setStatus('current')
panEntityFRUModuleTable = MibTable((1, 3, 6, 1, 4, 1, 25461, 1, 1, 7, 1, 2, 1), )
if mibBuilder.loadTexts: panEntityFRUModuleTable.setStatus('current')
panEntityFRUModuleEntry = MibTableRow((1, 3, 6, 1, 4, 1, 25461, 1, 1, 7, 1, 2, 1, 1), ).setIndexNames((0, "ENTITY-MIB", "entPhysicalIndex"))
if mibBuilder.loadTexts: panEntityFRUModuleEntry.setStatus('current')
panEntryFRUModulePowerUsed = MibTableColumn((1, 3, 6, 1, 4, 1, 25461, 1, 1, 7, 1, 2, 1, 1, 1), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: panEntryFRUModulePowerUsed.setStatus('current')
panEntryFRUModuleNumPorts = MibTableColumn((1, 3, 6, 1, 4, 1, 25461, 1, 1, 7, 1, 2, 1, 1, 2), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: panEntryFRUModuleNumPorts.setStatus('current')
panEntityFanTrayTable = MibTable((1, 3, 6, 1, 4, 1, 25461, 1, 1, 7, 1, 3, 1), )
if mibBuilder.loadTexts: panEntityFanTrayTable.setStatus('current')
panEntityFanTrayEntry = MibTableRow((1, 3, 6, 1, 4, 1, 25461, 1, 1, 7, 1, 3, 1, 1), ).setIndexNames((0, "ENTITY-MIB", "entPhysicalIndex"))
if mibBuilder.loadTexts: panEntityFanTrayEntry.setStatus('current')
panEntryFanTrayPowerUsed = MibTableColumn((1, 3, 6, 1, 4, 1, 25461, 1, 1, 7, 1, 3, 1, 1, 1), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: panEntryFanTrayPowerUsed.setStatus('current')
panEntityPowerSupplyTable = MibTable((1, 3, 6, 1, 4, 1, 25461, 1, 1, 7, 1, 4, 1), )
if mibBuilder.loadTexts: panEntityPowerSupplyTable.setStatus('current')
panEntityPowerSupplyEntry = MibTableRow((1, 3, 6, 1, 4, 1, 25461, 1, 1, 7, 1, 4, 1, 1), ).setIndexNames((0, "ENTITY-MIB", "entPhysicalIndex"))
if mibBuilder.loadTexts: panEntityPowerSupplyEntry.setStatus('current')
panEntryPowerSupplyPowerCapacity = MibTableColumn((1, 3, 6, 1, 4, 1, 25461, 1, 1, 7, 1, 4, 1, 1, 1), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: panEntryPowerSupplyPowerCapacity.setStatus('current')
panEntityMIBCompliances = MibIdentifier((1, 3, 6, 1, 4, 1, 25461, 1, 1, 7, 2, 1))
panEntityMIBGroups = MibIdentifier((1, 3, 6, 1, 4, 1, 25461, 1, 1, 7, 2, 2))
panEntityMIBCompliance = ModuleCompliance((1, 3, 6, 1, 4, 1, 25461, 1, 1, 7, 2, 1, 1)).setObjects(("PAN-ENTITY-EXT-MIB", "panEntityMIBChassisGroup"), ("PAN-ENTITY-EXT-MIB", "panEntityMIBFRUModuleGroup"), ("PAN-ENTITY-EXT-MIB", "panEntityMIBFanTrayGroup"), ("PAN-ENTITY-EXT-MIB", "panEntityMIBPowerSupplyGroup"))

if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    panEntityMIBCompliance = panEntityMIBCompliance.setStatus('current')
panEntityMIBChassisGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 25461, 1, 1, 7, 2, 2, 1)).setObjects(("PAN-ENTITY-EXT-MIB", "panEntityTotalPowerAvail"), ("PAN-ENTITY-EXT-MIB", "panEntityTotalPowerUsed"))
if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    panEntityMIBChassisGroup = panEntityMIBChassisGroup.setStatus('current')
panEntityMIBFRUModuleGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 25461, 1, 1, 7, 2, 2, 2)).setObjects(("PAN-ENTITY-EXT-MIB", "panEntryFRUModulePowerUsed"), ("PAN-ENTITY-EXT-MIB", "panEntryFRUModuleNumPorts"))
if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    panEntityMIBFRUModuleGroup = panEntityMIBFRUModuleGroup.setStatus('current')
panEntityMIBFanTrayGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 25461, 1, 1, 7, 2, 2, 3)).setObjects(("PAN-ENTITY-EXT-MIB", "panEntryFanTrayPowerUsed"))
if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    panEntityMIBFanTrayGroup = panEntityMIBFanTrayGroup.setStatus('current')
panEntityMIBPowerSupplyGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 25461, 1, 1, 7, 2, 2, 4)).setObjects(("PAN-ENTITY-EXT-MIB", "panEntryPowerSupplyPowerCapacity"))
if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    panEntityMIBPowerSupplyGroup = panEntityMIBPowerSupplyGroup.setStatus('current')
mibBuilder.exportSymbols("PAN-ENTITY-EXT-MIB", panEntityChassisGroup=panEntityChassisGroup, panEntityMIBPowerSupplyGroup=panEntityMIBPowerSupplyGroup, panEntityMIBFRUModuleGroup=panEntityMIBFRUModuleGroup, panEntityFanTrayGroup=panEntityFanTrayGroup, panEntityMIBObjects=panEntityMIBObjects, panEntityMIBCompliances=panEntityMIBCompliances, panEntityTotalPowerUsed=panEntityTotalPowerUsed, panEntryFRUModulePowerUsed=panEntryFRUModulePowerUsed, panEntityTotalPowerAvail=panEntityTotalPowerAvail, PYSNMP_MODULE_ID=panEntityMIBModule, panEntryFRUModuleNumPorts=panEntryFRUModuleNumPorts, panEntityPowerSupplyEntry=panEntityPowerSupplyEntry, panEntityMIBCompliance=panEntityMIBCompliance, panEntityPowerSupplyGroup=panEntityPowerSupplyGroup, panEntityFRUModuleEntry=panEntityFRUModuleEntry, panEntityFanTrayEntry=panEntityFanTrayEntry, panEntryFanTrayPowerUsed=panEntryFanTrayPowerUsed, panEntityPowerSupplyTable=panEntityPowerSupplyTable, panEntityFRUModuleTable=panEntityFRUModuleTable, panEntityMIBChassisGroup=panEntityMIBChassisGroup, panEntityMIBModule=panEntityMIBModule, panEntryPowerSupplyPowerCapacity=panEntryPowerSupplyPowerCapacity, panEntityFRUModuleGroup=panEntityFRUModuleGroup, panEntityMIBConformance=panEntityMIBConformance, panEntityMIBFanTrayGroup=panEntityMIBFanTrayGroup, panEntityMIBGroups=panEntityMIBGroups, panEntityFanTrayTable=panEntityFanTrayTable)
