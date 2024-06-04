# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [v0.0.1] - 2024-06-04

Evaluate transitive Providers! ↩️

## Added

- Factory/Singleton now evaluate Provider arguments at runtime

## Changed

- Renamed `BlankProvider` -> `Blank`
- Moved providers into dedicated package

## Fixed

- Broken example in examples/simple_service

### Closes

## [v0.0.0] - 2024-06-03

Pre Release! 🚀

### Added

- Wiring via `@wiring.inject` or `wiring.wire()`
- Providers for injection
    - BlankProvider
    - ExistingSingleton
    - Singleton
    - Factory
- Overriding providers with context managers
- Simple service example to examples/

### Changed

### Fixed

### Closes
