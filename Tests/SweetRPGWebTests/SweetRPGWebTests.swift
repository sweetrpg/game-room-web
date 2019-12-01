import XCTest
@testable import web

final class webTests: XCTestCase {
    func testExample() {
        // This is an example of a functional test case.
        // Use XCTAssert and related functions to verify your tests produce the correct
        // results.
        XCTAssertEqual(web().text, "Hello, World!")
    }

    static var allTests = [
        ("testExample", testExample),
    ]
}
