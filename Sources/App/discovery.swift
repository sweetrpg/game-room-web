//
// Created by Paul Schifferer on 6/23/21.
//

import Foundation
import Vapor
import Common


func lookup(service : String) throws {
}

func register(_ app : Application) throws {
    let instanceName = Constants.serviceIdBase + (Host.current().address ?? "localhost")
    try ConsulServiceRegistryUtils.register(instanceName: instanceName,
            serviceName: Constants.serviceName,
            application: app)
}

func discovery(_ app : Application) throws {
    try register(app)
//    try lookup(service: Common.Constants.libraryAPIServiceName)
}
