// swift-tools-version:5.4

import PackageDescription


let package = Package(
        name: "sweetrpg-web",
        platforms: [
            .macOS(.v10_15),
        ],
        dependencies: [
            // 💧 A server-side Swift web framework.
            .package(url: "https://github.com/vapor/vapor.git", from: "4.0.0"),
            .package(url: "https://github.com/vapor/fluent.git", from: "4.0.0"),
            .package(url: "https://github.com/vapor/fluent-mongo-driver.git", from: "1.0.0"),
            .package(url: "https://github.com/vapor/leaf.git", from: "4.0.0"),
            .package(url: "https://github.com/vapor/jwt.git", from: "4.0.0"),
            .package(url: "https://github.com/vapor-community/sendgrid.git", from: "4.0.0"),
            .package(url: "https://github.com/vapor/redis.git", from: "4.0.0"),
            // .package(name: "sweetrpg-users-model", path: "../UsersModel"),
            .package(name: "sweetrpg-common", path: "../Common"),
        ],
        targets: [
            .target(
                    name: "App",
                    dependencies: [
                        .product(name: "SweetRPGCommon", package: "sweetrpg-common"),
                        .product(name: "Fluent", package: "fluent"),
                        .product(name: "FluentMongoDriver", package: "fluent-mongo-driver"),
                        .product(name: "Leaf", package: "leaf"),
//                        .product(name: "JWT", package: "jwt"),
                        .product(name: "Vapor", package: "vapor"),
//                        .product(name: "ImperialGoogle", package: "Imperial"),
//                        .product(name: "ImperialGitHub", package: "Imperial"),
//                        .product(name: "SendGrid", package: "sendgrid"),
                        .product(name: "Redis", package: "redis"),
                    ],
                    swiftSettings: [
                        // Enable better optimizations when building in Release configuration. Despite the use of
                        // the `.unsafeFlags` construct required by SwiftPM, this flag is recommended for Release
                        // builds. See <https://github.com/swift-server/guides/blob/main/docs/building.md#building-for-production> for details.
                        .unsafeFlags([ "-cross-module-optimization" ], .when(configuration: .release)),
                    ]
            ),
            .executableTarget(name: "Run", dependencies: [ .target(name: "App") ]),
            .testTarget(name: "AppTests", dependencies: [
                .target(name: "App"),
                .product(name: "XCTVapor", package: "vapor"),
            ]),
        ]
)

// Prometheus
// Logging
// Stripe
// Auth0
// APM (NewRelic?)
// Sentry?
