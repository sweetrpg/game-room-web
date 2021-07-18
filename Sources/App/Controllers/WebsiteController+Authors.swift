//
// WebsiteController+Index.swift
// Copyright (c) 2021 Paul Schifferer.
//

import Leaf
import Vapor
import ProfilesModel
import LibraryModel


extension WebsiteController {
    func addAuthorRoutes(to routes : RoutesBuilder) {
        let authorRoutes = routes.grouped("authors")
        authorRoutes.get(use: getAuthorsHandler)
        authorRoutes.get(":authorId", use: getAuthorHandler)
    }

    func getAuthorsHandler(_ req : Request) -> EventLoopFuture<View> {
        let context = AuthorsContext(title: "Authors",
                authors: [
                    Author(name: "A1"),
                    Author(name: "A3"),
                    Author(name: "A2"),
                ])
        return req.view.render("authors", context)
    }

    func getAuthorHandler(_ req : Request) throws -> EventLoopFuture<View> {
        guard let authorId = req.parameters.get("authorId") else {
            throw Abort(.badRequest)
        }
        let context = AuthorContext(title: "Author - A1", author: Author(name: "A1"))
        return req.view.render("author", context)
    }
}

struct AuthorsContext : Encodable {
    let title : String
    let authors : [Author]
}

struct AuthorContext : Encodable {
    let title : String
    let author : Author
}
