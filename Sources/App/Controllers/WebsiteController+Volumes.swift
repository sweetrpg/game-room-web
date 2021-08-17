//
// WebsiteController+Volumes.swift
// Copyright (c) 2021 Paul Schifferer.
//

import Leaf
import Vapor
import ProfilesModel
import LibraryModel
import SDK


extension WebsiteController {
    func addVolumeRoutes(to routes : RoutesBuilder) {
        let volumeRoutes = routes.grouped("volumes")
        volumeRoutes.get(use: getVolumesHandler)
        volumeRoutes.get(":volumeId", use: getVolumeHandler)
    }

    func getVolumesHandler(_ req : Request) throws -> EventLoopFuture<View> {
//        let system = LibraryModel.System(id: UUID(), gameSystemIdentifier: "dnd", editionIdentifier: "5")
//        let pagination = getPagination(from: req)
        let volumesReq = SDK.Volumes.all(range: .startingAt(offset: 0 /*pagination.offset*/, limit: 50 /*pagination.limit*/))
         return client.run(volumesReq) { result in
             let context = VolumesContext(title: "Volumes",
                     prefix: getPrefix(from: req),
                     volumes: result.value /*[
                    Volume(name: "V1", systemId: try system.requireID()),
                    Volume(name: "V3", systemId: try system.requireID()),
                    Volume(name: "V2", systemId: try system.requireID()),
                ]*/)
             return req.view.render("volumes", context)
        }

    }

    func getVolumeHandler(_ req : Request) throws -> EventLoopFuture<View> {
//        let system = LibraryModel.System(id: UUID(), gameSystemIdentifier: "dnd", editionIdentifier: "5")
    let volumeId = req.parameters.get("volumeId")
    let volume = SDK.Volumes.volume(volumeId)
        let context = VolumeContext(title: "Volume - V1",
                prefix: getPrefix(from: req),
                volume: volume /*Volume(name: "V1", systemId: try system.requireID())*/)
        return req.view.render("volume", context)
    }
}

struct VolumesContext : Encodable {
    let title : String
    let prefix : String = "/"
    let volumes : [Volume]
}

struct VolumeContext : Encodable {
    let title : String
    let prefix : String = "/"
    let volume : Volume
}
