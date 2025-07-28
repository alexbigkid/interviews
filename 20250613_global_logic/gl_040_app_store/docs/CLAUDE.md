# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a mobile CI/CD demonstration repository containing iOS and Android Hello World applications with automated deployment pipelines using GitHub Actions and Fastlane. The project demonstrates enterprise-level DevOps practices with separated build and deployment stages, quality gates, and artifact promotion.

## Key Architecture

### Dual-Platform Structure
- **ios-hello-world/**: Swift-based iOS application with Xcode project
- **android-hello-world/**: Kotlin-based Android application with Gradle build system
- **Separated CI/CD Pipelines**: Independent workflows for each platform with test-first approach

### Pipeline Architecture
The project uses a **4-workflow separated pipeline approach**:
1. **ios-build.yml**: Tests always run, builds and TestFlight deployment on version tags
2. **ios-deploy.yml**: Manual production deployment using pre-built artifacts  
3. **android-build.yml**: Tests always run, builds and Play Store beta deployment on version tags
4. **android-deploy.yml**: Manual production deployment to different Play Store tracks

### Version Management
- **iOS**: Managed in `HelloWorld.xcodeproj/project.pbxproj` via Fastlane actions
- **Android**: Managed in `android-hello-world/app/build.gradle` via string replacement
- **Automatic Tagging**: Creates `v1.2.3-ios` and `v1.2.3-android` tags after successful releases

## Common Commands

### iOS Development
```bash
cd ios-hello-world
bundle install
bundle exec fastlane test        # Run unit tests
bundle exec fastlane build       # Build app for testing
bundle exec fastlane beta        # Build and deploy to TestFlight
bundle exec fastlane release     # Build and deploy to App Store
```

### Android Development  
```bash
cd android-hello-world
bundle install
bundle exec fastlane test           # Run unit tests
bundle exec fastlane build_debug    # Build debug APK
bundle exec fastlane build_release  # Build signed release APK
bundle exec fastlane beta           # Build and deploy to Play Store beta
bundle exec fastlane deploy         # Build and deploy to Play Store production
```

### Deployment Triggers
```bash
# iOS releases (triggers automated TestFlight deployment)
git tag ios-patch && git push origin ios-patch    # 1.0.0 → 1.0.1
git tag ios-minor && git push origin ios-minor    # 1.0.0 → 1.1.0  
git tag ios-major && git push origin ios-major    # 1.0.0 → 2.0.0

# Android releases (triggers automated Play Store beta deployment)
git tag android-patch && git push origin android-patch
git tag android-minor && git push origin android-minor
git tag android-major && git push origin android-major
```

## Key Development Concepts

### Quality Gates
- Tests must pass before any release builds or deployments
- Release jobs depend on successful test job completion
- Version tags only trigger deployment if tests pass

### Artifact Promotion
- Build once, deploy multiple times from same artifact
- Production deployments use pre-built artifacts from build stage
- Manual production deployment prevents accidental releases

### Platform Constraints
- **iOS**: Requires macOS runners for building (Xcode dependency)
- **Android**: Can use Linux runners throughout entire pipeline
- **iOS Deployment Alternative**: Pre-built IPAs can be deployed from Linux using App Store Connect API

### Security Model
- All sensitive data stored in GitHub Secrets
- Automatic cleanup of temporary credential files
- No keystores or certificates committed to repository
- App-specific passwords required for Apple ID authentication

## File Structure Significance

### Core Application Files
- `ios-hello-world/HelloWorld.xcodeproj/`: Xcode project with version info
- `android-hello-world/app/build.gradle`: Android build config with version info
- `**/fastlane/Fastfile`: Platform-specific deployment automation

### CI/CD Configuration
- `.github/workflows/`: Four separate workflow files implementing separated build/deploy pattern
- `docs/DEPLOYMENT.md`: Complete setup guide with required secrets and configuration
- `README.md`: Comprehensive architecture documentation with Mermaid diagrams

### Dependencies
- `Gemfile`: Ruby/Fastlane dependencies in each platform directory
- No package.json or other dependency managers present

This repository is designed as a DevOps demonstration showing production-ready mobile CI/CD practices with proper separation of concerns, quality gates, and security considerations.

## Additional Documentation

### Traditional Deployment Guides
- **[TRADITIONAL_IOS_DEPLOYMENT.md](TRADITIONAL_IOS_DEPLOYMENT.md)**: Comprehensive guide to manual iOS App Store deployment process (without Fastlane), including detailed Mermaid diagrams, real-world examples, troubleshooting, and comparison with automated approaches

- **[TRADITIONAL_ANDROID_DEPLOYMENT.md](TRADITIONAL_ANDROID_DEPLOYMENT.md)**: Complete guide to manual Android Google Play Store deployment process (without Fastlane), featuring extensive Mermaid diagrams, real-world TaskMaster app example, AAB/APK signing, Play Console configuration, release management, and traditional vs automated comparison

### Fastlane Automation Guides
- **[FASTLANE_IOS_DEPLOYMENT.md](FASTLANE_IOS_DEPLOYMENT.md)**: Complete Fastlane automation guide for iOS App Store deployment, covering installation, configuration, match certificate management, CI/CD integration, screenshot automation, and best practices with real-world TaskMaster example

- **[FASTLANE_ANDROID_DEPLOYMENT.md](FASTLANE_ANDROID_DEPLOYMENT.md)**: Comprehensive Fastlane automation guide for Android Google Play Store deployment, including setup, Google Play service account configuration, build automation, release track management, CI/CD integration, and performance optimization

### Automation Strategy & Decision Making
- **[AUTOMATION_DECISION_MATRIX.md](AUTOMATION_DECISION_MATRIX.md)**: Strategic framework for making data-driven automation decisions using visual matrices and ROI analysis. Includes frequency, effort, complexity, and ROI evaluation with real-world examples, implementation strategies, team decision processes, and success metrics

### Reference Guides
- **[FASTLANE_ACTIONS_REFERENCE.md](FASTLANE_ACTIONS_REFERENCE.md)**: Complete reference guide for Fastlane actions and tools for iOS and Android platforms. Covers platform-specific differences, authentication methods (Apple ID vs API Key vs Service Account JSON), syntax examples, and common usage patterns. Includes detailed comparison between iOS actions (pilot, deliver, match, cert, sigh) and Android actions (supply, gradle, screengrab)

- **[PRINCIPLES_SOLID.md](PRINCIPLES_SOLID.md)**: Quick reference to SOLID software design principles with definitions and short explanations. Covers Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion principles with practical guidelines

- **[PRINCIPLES_TDD_ZOMBIES.md](PRINCIPLES_TDD_ZOMBIES.md)**: Guide to the ZOMBIES approach for Test-Driven Development (TDD) test ordering. Covers the systematic progression from Zero/empty cases through One, Many, Boundary, Interface, Exception, and Simple scenarios with TDD best practices