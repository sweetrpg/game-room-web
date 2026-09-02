## [0.11.0] - 2026-09-02

### 🚀 Features

- *(library)* Confirm before removing a library entry

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.10.1
- Start library-aligned-remove-button (#416)
## [0.10.1] - 2026-09-01

### 🐛 Bug Fixes

- *(landing)* Treat Go zero-time / epoch dates as no date

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.10.0
## [0.10.0] - 2026-09-01

### 🚀 Features

- *(game-room)* Detail-page redesign, rich visibility tooltips, name-search add-volume

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.9.0
## [0.9.0] - 2026-09-01

### 🚀 Features

- *(tables)* Icon visibility picker for table creation

### 🐛 Bug Fixes

- *(landing)* Wishlist card counts wishlists, not aggregated entries
- Correct name for profile menu item

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.8.1
## [0.8.1] - 2026-09-01

### 🐛 Bug Fixes

- *(k8s)* Web-v1 Service ClusterIP, not LoadBalancer

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.8.0
## [0.8.0] - 2026-09-01

### 🚀 Features

- *(wishlist)* Icon-only detail actions, collapsed add-volume, min-length search

### ⚙️ Miscellaneous Tasks

- We don't use Segment
- Really, we don't use Segment
- *(release)* Merge master into develop after v0.7.3
- Finish removing Segment analytics
## [0.7.3] - 2026-09-01

### 🐛 Bug Fixes

- Restore constants.SEGMENT_WRITE_KEY

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.7.2
## [0.7.2] - 2026-09-01

### 🐛 Bug Fixes

- Add response code to 400 error
- *(auth)* Call users-api /profile, not /api/profile

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.7.1
- More error constants
## [0.7.1] - 2026-09-01

### 🐛 Bug Fixes

- *(k8s)* Set USERS_API_URL in the dev configmap

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.7.0
## [0.7.0] - 2026-08-31

### 🚀 Features

- *(auth)* Resolve canonical user id from users-api profile

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.6.1
## [0.6.1] - 2026-08-31

### 🐛 Bug Fixes

- Update template text and translations for consistency
- Wishlist assertion

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.6.0
- Remove unused blueprints
- Remove commented code
## [0.6.0] - 2026-08-30

### 🚀 Features

- *(library)* Add per-entry visibility menu with confirmation (#418)
- *(library)* Localize effective visibility labels and icons
- *(library)* Add aligned destructive remove button with confirmation (#416)
- *(library)* Add multi-select bulk visibility override (#414)

### 🐛 Bug Fixes

- *(wishlist)* Polish wishlist browse cards and confirm delete
- Unit tests
- Write route tests

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.5.0
- Re-sync
## [0.5.0] - 2026-08-30

### 🚀 Features

- *(wishlists)* Add multi-wishlist support
- *(wishlists)* Add create wishlist action to landing card

### 🐛 Bug Fixes

- *(redirects)* Carry APPLICATION_BASE_PATH prefix through in-app redirects

### 💼 Other

- Merge develop into fix/redirect-base-path-prefix

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.4.2
- Update wishlist label
- Add ruff as a dev dependency
## [0.4.2] - 2026-08-29

### 🐛 Bug Fixes

- *(landing)* Address review feedback on card actions and add visibility menu
- *(library)* Use catalog-api's new /volumes/search endpoint

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.4.1
## [0.4.1] - 2026-08-29

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.4.0
## [0.4.0] - 2026-08-29

### 🚀 Features

- *(landing)* Add quick-create actions to library/tables landing cards

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.3.4
## [0.3.4] - 2026-08-29

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.3.3
## [0.3.3] - 2026-08-29

### 🐛 Bug Fixes

- Move banner above main content, pin landing footer to viewport bottom

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.3.2
## [0.3.2] - 2026-08-28

### 🐛 Bug Fixes

- Hide the avatar-initial fallback once the gravatar image loads

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.3.1
## [0.3.1] - 2026-08-28

### 🐛 Bug Fixes

- Forward the caller's access token to game-room-api

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.3.0
## [0.3.0] - 2026-08-28

### 🚀 Features

- Gate the landing page on login, populate cards with real data

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.2.1
- Update to standard labels
## [0.2.1] - 2026-08-28

### 🐛 Bug Fixes

- Match header avatar menu and app switcher to the established platform convention

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.2.0
## [0.2.0] - 2026-08-28

### 🚀 Features

- Add missing footer to the landing page

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.1.10
## [0.1.10] - 2026-08-28

### 🐛 Bug Fixes

- Don't crash logged-in requests when SEGMENT_WRITE_KEY is unset

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.1.9
## [0.1.9] - 2026-08-28

### 🐛 Bug Fixes

- Set SHARED_URL, missing entirely
- Drop trailing slash from APPLICATION_BASE_PATH
- Reflect real login state via the suite-wide shared session

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.1.8
## [0.1.8] - 2026-08-28

### 🐛 Bug Fixes

- Use Flask(__name__) instead of a hyphenated app name string

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.1.7
## [0.1.7] - 2026-08-28

### 🐛 Bug Fixes

- Add missing REDIS_HOST, correct wrong game-room-api port
- Pass REDIS_PASS to session and cache Redis connections

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.1.6
## [0.1.6] - 2026-08-28

### 🐛 Bug Fixes

- Pod crash-loop on boot (dead logstash formatter, wrong CACHE_TYPE)

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.1.5
## [0.1.5] - 2026-08-28

### 🐛 Bug Fixes

- *(ci)* Grant docs job write permission to publish gh-pages
- Bump sweetrpg-client to 0.1.2, fixing the distutils import crash

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.1.4
## [0.1.4] - 2026-08-27

### 🐛 Bug Fixes

- Remove web-auth secret ref

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.1.3
## [0.1.3] - 2026-08-27

### 🐛 Bug Fixes

- Indentation

### 🚜 Refactor

- *(secrets)* Consolidate and share Redis credentials across game-room dev

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.1.2
## [0.1.2] - 2026-08-27

### 🐛 Bug Fixes

- *(kubernetes)* Remove dead newrelic.ini config mount

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.1.1
## [0.1.1] - 2026-08-26

### 🐛 Bug Fixes

- *(ci)* Bring workflows in line with shared github-actions pattern
- *(kubernetes)* Remove dead init-templates init container

### 🧪 Testing

- Cover library/wishlist/tables write routes and game_room_client

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.1.0
- Update k8s manifests
- More k8s updates
## [0.1.0] - 2026-08-26

### 🚀 Features

- *(shelf-web)* Add admin-api-client for maintenance-mode support
- *(shelf)* Build library/wishlist/table UI against shelf-api
- *(shelf)* Add viewer routes for another user's library/wishlist/tables

### 🐛 Bug Fixes

- Secret version
- *(k8s)* Remove HPA and PDB from dev overlay
- *(ci)* Scope Docker Build's concurrency group by ref
- *(deps)* Pin sweetrpg-game-room-objects to its real published version
- Rename kubernetes manifests from library to game-room, fill deploy gaps

### 🚜 Refactor

- Rename library-web to shelf-web
- Rename shelf-web references to game-room-web
- Rename remaining shelf references to game-room

### ⚙️ Miscellaneous Tasks

- Build arm64 image alongside amd64
- Fix memory spec
- Reloader, pod monitor
- Rename license file
- *(dev)* Remove unused Istio resources and update namespace
- Add annotations for flagd
- Update Python version
- Bump to Python 3.14 (platform minimum)
- Bring repo up to sweetrpg scaffolding standard
- Migrate Python packaging and CI to uv
- Add release workflows, drop legacy Vue frontend and semantic-release tag job
# Changelog

<!--next-version-placeholder-->

## v0.0.106 (2022-12-20)


## v0.0.105 (2022-12-17)


## v0.0.104 (2022-08-15)


## v0.0.103 (2022-03-10)


## v0.0.102 (2022-03-10)


## v0.0.101 (2022-03-10)


## v0.0.100 (2022-03-10)


## v0.0.99 (2022-03-09)


## v0.0.98 (2022-03-09)


## v0.0.97 (2022-03-09)


## v0.0.96 (2022-03-09)


## v0.0.95 (2022-03-09)


## v0.0.94 (2022-03-09)


## v0.0.93 (2022-03-09)


## v0.0.92 (2022-03-09)


## v0.0.91 (2022-02-11)


## v0.0.90 (2022-02-11)


## v0.0.89 (2022-02-07)


## v0.0.88 (2022-02-07)


## v0.0.87 (2022-02-07)


## v0.0.86 (2022-02-06)


## v0.0.85 (2022-02-06)


## v0.0.84 (2022-02-06)


## v0.0.83 (2022-02-06)


## v0.0.82 (2022-02-06)


## v0.0.81 (2022-01-31)


## v0.0.80 (2022-01-31)


## v0.0.79 (2022-01-31)


## v0.0.78 (2022-01-31)


## v0.0.77 (2022-01-31)


## v0.0.76 (2022-01-15)


## v0.0.75 (2022-01-15)


## v0.0.74 (2022-01-15)


## v0.0.73 (2022-01-15)


## v0.0.72 (2022-01-15)


## v0.0.71 (2022-01-15)


## v0.0.70 (2022-01-14)


## v0.0.69 (2022-01-10)


## v0.0.68 (2022-01-10)


## v0.0.67 (2022-01-08)


## v0.0.66 (2022-01-08)


## v0.0.65 (2022-01-08)


## v0.0.64 (2022-01-08)


## v0.0.63 (2022-01-08)


## v0.0.62 (2022-01-08)


## v0.0.61 (2022-01-08)


## v0.0.60 (2022-01-08)


## v0.0.59 (2021-12-27)


## v0.0.58 (2021-12-27)


## v0.0.57 (2021-12-27)


## v0.0.56 (2021-12-27)


## v0.0.55 (2021-12-24)


## v0.0.54 (2021-12-24)


## v0.0.53 (2021-12-24)


## v0.0.52 (2021-12-24)


## v0.0.51 (2021-12-24)


## v0.0.50 (2021-12-15)


## v0.0.49 (2021-12-15)


## v0.0.48 (2021-12-14)


## v0.0.47 (2021-12-14)


## v0.0.46 (2021-12-14)


## v0.0.45 (2021-12-14)


## v0.0.44 (2021-12-12)


## v0.0.43 (2021-12-12)


## v0.0.42 (2021-12-12)


## v0.0.41 (2021-12-12)


## v0.0.40 (2021-12-11)


## v0.0.39 (2021-12-11)


## v0.0.38 (2021-12-11)


## v0.0.37 (2021-12-11)


## v0.0.36 (2021-12-11)


## v0.0.35 (2021-12-06)


## v0.0.34 (2021-12-06)


## v0.0.33 (2021-12-06)


## v0.0.32 (2021-12-06)


## v0.0.31 (2021-11-27)


## v0.0.30 (2021-11-27)


## v0.0.29 (2021-11-27)


## v0.0.28 (2021-11-27)


## v0.0.27 (2021-11-13)


## v0.0.26 (2021-11-13)


## v0.0.25 (2021-11-13)


## v0.0.24 (2021-11-13)


## v0.0.23 (2021-11-12)


## v0.0.22 (2021-11-12)


## v0.0.21 (2021-11-12)


## v0.0.20 (2021-11-12)


## v0.0.19 (2021-11-11)


## v0.0.18 (2021-11-11)


## v0.0.17 (2021-11-11)


## v0.0.16 (2021-11-11)


## v0.0.15 (2021-11-11)


## v0.0.14 (2021-11-11)


## v0.0.13 (2021-11-11)


## v0.0.12 (2021-11-11)


## v0.0.11 (2021-11-11)


## v0.0.10 (2021-11-11)


## v0.0.9 (2021-11-09)


## v0.0.8 (2021-11-09)


## v0.0.7 (2021-11-08)


## v0.0.6 (2021-11-08)


## v0.0.5 (2021-11-08)


## v0.0.4 (2021-11-08)


## v0.0.3 (2021-11-08)


## v0.0.2 (2021-11-06)


## v0.0.1 (2021-11-04)

