import Vapor
import Common


struct LibraryHealthInfo : HealthInfo, Content {
    let timestamp : Date
    let dbHealthy : Bool
}

func healthCallback() -> LibraryHealthInfo {
    return LibraryHealthInfo(timestamp: Date(), dbHealthy: true)
}
