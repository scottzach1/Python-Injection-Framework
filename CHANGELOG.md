# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [v0.0.2] - 2024-06-12

Add language support for 3.10! 🐍

## Added

- Language support for Python 3.10
    - Drop 3.12 generics syntax usage
    - Drop typing.Self usage
    - Add matrix testing for 3.10, 3.11, 3.12 versions

## Changed

- Publish badges only on tags pipeline

## Fixed

- Circular imports bug for wiring.intercept
- Small documentation changes

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
