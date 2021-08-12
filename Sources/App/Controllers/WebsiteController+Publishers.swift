//
// WebsiteController+Index.swift
// Copyright (c) 2021 Paul Schifferer.
//

import Leaf
import Vapor
import ProfilesModel
import LibraryModel


extension WebsiteController {
    func addPublisherRoutes(to routes : RoutesBuilder) {
        let publisherRoutes = routes.grouped("publishers")
        publisherRoutes.get(use: getPublishersHandler)
        publisherRoutes.get(":publisherId", use: getPublisherHandler)
    }

    func getPublishersHandler(_ req : Request) -> EventLoopFuture<View> {
        let context = PublishersContext(title: "Publishers",
                prefix: getPrefix(from: req),
                publishers: [
                    Publisher(name: "P1"),
                    Publisher(name: "P3"),
                    Publisher(name: "P2"),
                ])
        return req.view.render("publishers", context)
    }

    func getPublisherHandler(_ req : Request) -> EventLoopFuture<View> {
        let context = PublisherContext(title: "Publisher - P1",
                prefix: getPrefix(from: req),
                publisher: Publisher(name: "P1"))
        return req.view.render("publisher", context)
    }
}

struct PublishersContext : Encodable {
    let title : String
    let prefix : String = "/"
    let publishers : [Publisher]
}

struct PublisherContext : Encodable {
    let title : String
    let prefix : String = "/"
    let publisher : Publisher
}
