import XCTest

import webTests

var tests = [XCTestCaseEntry]()
tests += webTests.allTests()
XCTMain(tests)
