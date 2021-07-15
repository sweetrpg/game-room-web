//
// WebsiteController+Index.swift
// Copyright (c) 2021 Paul Schifferer.
//

import Leaf
import Vapor
import ProfilesModel
import LibraryModel


extension WebsiteController {
    func addVolumeRoutes(_ routes : RoutesBuilder) {
        let volumeRoutes = routes.grouped("volumes")
        volumeRoutes.get(use: getVolumesHandler)
        volumeRoutes.get(":volumeId", use: getVolumeHandler)
    }

    func getVolumesHandler(_ req : Request) -> EventLoopFuture<View> {
        let context = VolumesContext(title: "Volumes",
                volumes: [
                    Volume(name: "V1"),
                    Volume(name: "V3"),
                    Volume(name: "V2"),
                ])
        return req.view.render("volumes", context)
    }

    func getVolumeHandler(_ req : Request) -> EventLoopFuture<View> {
        let context = VolumeContext(title: "Volume - V1", volume: Volume(name: "V1"))
        return req.view.render("volume", context)
    }
}

struct VolumesContext : Encodable {
    let title : String
    let volumes : [Volume]
}

struct VolumeContext : Encodable {
    let title : String
    let volume : Volume
}
