# Mobile App Deployment Setup

This repository contains iOS and Android Hello World apps with automated deployment using GitHub Actions and Fastlane.

## GitHub Secrets Configuration

### Required Secrets for iOS Deployment

Add these secrets to your GitHub repository settings (`Settings > Secrets and variables > Actions`):

| Secret Name | Description |
|-------------|-------------|
| `APPLE_ID` | Your Apple ID email address |
| `APPLE_TEAM_ID` | Your Apple Developer Team ID |
| `IOS_BUNDLE_IDENTIFIER` | iOS app bundle identifier (e.g., `com.example.HelloWorld`) |
| `FASTLANE_USER` | Your Apple ID email (usually same as APPLE_ID) |
| `FASTLANE_PASSWORD` | App-specific password for your Apple ID |
| `FASTLANE_APPLE_APPLICATION_SPECIFIC_PASSWORD` | App-specific password (same as above) |
| `MATCH_PASSWORD` | Password for fastlane match (certificate management) |

### Required Secrets for Android Deployment

| Secret Name | Description |
|-------------|-------------|
| `ANDROID_PACKAGE_NAME` | Android app package name (e.g., `com.example.helloworld`) |
| `GOOGLE_PLAY_JSON_KEY_DATA` | Google Play Console service account JSON key (entire file content) |
| `ANDROID_KEYSTORE_DATA` | Android keystore file encoded in base64 |
| `ANDROID_KEYSTORE_PASSWORD` | Password for the Android keystore |
| `ANDROID_KEY_ALIAS` | Alias name for the signing key |
| `ANDROID_KEY_PASSWORD` | Password for the signing key |

## Version Management

### Version File Locations

**iOS**: Version numbers are stored in the Xcode project file:
- File: `ios-hello-world/HelloWorld.xcodeproj/project.pbxproj`
- Properties: `CFBundleShortVersionString` (marketing version) and `CFBundleVersion` (build number)
- Updated via: fastlane's `increment_version_number` and `increment_build_number` actions

**Android**: Version numbers are stored in the Gradle build file:
- File: `android-hello-world/app/build.gradle`  
- Properties: `versionName` (marketing version) and `versionCode` (build number)
- Updated via: direct string replacement in the build pipeline

### Automatic Version Tags

After successful builds and deployments, the pipeline automatically creates git tags:
- **iOS**: `v1.2.3-ios` (includes marketing version and platform)
- **Android**: `v1.2.3-android` (includes marketing version and platform)

These tags provide a clear audit trail of all releases and can be used for:
- Tracking what version is deployed where
- Creating release notes
- Rollback references
- Compliance and audit requirements

## Setup Instructions

### iOS Setup

1. **Apple Developer Account**: Ensure you have an active Apple Developer account
2. **App Store Connect**: Create your app in App Store Connect
3. **App-Specific Password**: Generate an app-specific password for your Apple ID:
   - Go to [appleid.apple.com](https://appleid.apple.com)
   - Sign in > Security > App-Specific Passwords
   - Generate a new password for "Fastlane"
4. **Fastlane Match**: Set up certificate management (optional but recommended)

### Android Setup

1. **Google Play Console**: Create your app in Google Play Console
2. **Service Account**: Create a service account for API access:
   - Go to Google Cloud Console
   - Create a service account with Google Play Developer API access
   - Download the JSON key file
3. **Android Keystore**: Generate a signing keystore:
   ```bash
   keytool -genkey -v -keystore android-keystore.jks -keyalg RSA -keysize 2048 -validity 10000 -alias your-key-alias
   ```
4. **Base64 Encode Keystore**: Convert keystore to base64:
   ```bash
   base64 -i android-keystore.jks
   ```

## Deployment Triggers

### Automatic Deployment

1. **Push to main branch**: Triggers deployment without version bump for both platforms
2. **Path-based deployment**: Only deploys when relevant files change
   - iOS: Changes to `ios-hello-world/**` or iOS workflow file
   - Android: Changes to `android-hello-world/**` or Android workflow file
3. **Tag-based deployment**: Push platform-specific tags to trigger deployment with version bump

#### iOS Deployment Tags
```bash
# iOS Patch version bump (1.0.0 → 1.0.1)
git tag ios-patch && git push origin ios-patch

# iOS Minor version bump (1.0.0 → 1.1.0)
git tag ios-minor && git push origin ios-minor

# iOS Major version bump (1.0.0 → 2.0.0)
git tag ios-major && git push origin ios-major
```

#### Android Deployment Tags
```bash
# Android Patch version bump (1.0.0 → 1.0.1)
git tag android-patch && git push origin android-patch

# Android Minor version bump (1.0.0 → 1.1.0)
git tag android-minor && git push origin android-minor

# Android Major version bump (1.0.0 → 2.0.0)
git tag android-major && git push origin android-major
```

### Manual Deployment

#### Production Deployment Process

1. **Build Phase** (automatic on version tags):
   ```bash
   # Trigger iOS build and TestFlight deployment
   git tag ios-patch && git push origin ios-patch
   
   # Trigger Android build and Beta deployment  
   git tag android-minor && git push origin android-minor
   ```

2. **Production Deployment** (manual via GitHub Actions):
   - Go to "Actions" tab in GitHub
   - Select "iOS Deploy to App Store" or "Android Deploy to Play Store"
   - Click "Run workflow"
   - Enter the build number from the previous build
   - Select deployment environment (production/testflight/beta/etc.)
   - Click "Run workflow"

#### Manual Build Triggers

- **iOS Build and Test**: Manual trigger with optional version bump
- **Android Build and Test**: Manual trigger with optional version bump

## Workflow Overview

There are **four separate GitHub Actions workflows** following CI/CD best practices with separated build and deployment stages:

### iOS Build Pipeline (`ios-build.yml`)

**Triggers:** Push/PR to main/develop, iOS tags, manual dispatch

1. **Test Job** (always runs on every push/PR):
   - Sets up macOS environment with Xcode
   - Runs unit tests using fastlane
   - Builds app for testing
   - Uploads test results and artifacts
   - **Must pass for release job to proceed**

2. **Build and Deploy to TestFlight Job** (runs only on version tags + tests pass):
   - Depends on test job success
   - Installs certificates and provisioning profiles  
   - Bumps version number based on tag type
   - Builds signed release archive
   - **Automatically deploys to TestFlight**
   - Uploads release artifact for later App Store deployment
   - Commits version bump back to repository
   - **Creates version tag** (e.g., `v1.2.3-ios`) for tracking releases

### iOS Deployment Pipeline (`ios-deploy.yml`)

**Triggers:** Manual workflow dispatch only

- Downloads previously built artifact by build number
- Deploys to either:
  - **TestFlight**: For additional TestFlight deployment
  - **App Store Production**: Manual deployment to App Store (requires review)

### Android Build Pipeline (`android-build.yml`)

**Triggers:** Push/PR to main/develop, Android tags, manual dispatch

1. **Test Job** (always runs on every push/PR):
   - Sets up Java and Android SDK
   - Runs unit tests using fastlane
   - Builds debug APK
   - Uploads test results and debug artifacts
   - **Must pass for release job to proceed**

2. **Build and Deploy to Beta Job** (runs only on version tags + tests pass):
   - Depends on test job success
   - Sets up signing certificates and service account
   - Bumps version in build.gradle based on tag type
   - Builds signed release AAB
   - **Automatically deploys to Google Play Beta track**
   - Uploads release artifact for later production deployment
   - Commits version bump back to repository
   - **Creates version tag** (e.g., `v1.2.3-android`) for tracking releases

### Android Deployment Pipeline (`android-deploy.yml`)

**Triggers:** Manual workflow dispatch only

- Downloads previously built artifact by build number
- Deploys to Google Play tracks:
  - **Internal**: Internal testing
  - **Alpha**: Alpha testing track
  - **Beta**: Beta testing track  
  - **Production**: Production release (as draft requiring manual review)

### Key Benefits of Separated Pipelines

- **Test-First Approach**: Tests always run on every push, builds only happen on release tags
- **Quality Gates**: Release builds and deployments only proceed if tests pass
- **Artifact Promotion**: Build once, deploy multiple times from same artifact
- **Independent Stages**: Test failures prevent release builds and deployments
- **Manual Production Control**: Production deployments require explicit approval
- **Environment Protection**: GitHub environments can be configured with required reviewers
- **Audit Trail**: Clear separation between automated builds and manual deployments
- **Resource Efficiency**: Tests run on every push, releases only on tags
- **Rollback Capability**: Can redeploy any previous build number
- **Fail Fast**: Quick feedback on test failures without wasting build resources
- **Version Tracking**: Automatic version tags created for every release (e.g., `v1.2.3-ios`, `v1.2.3-android`)

## Local Development

### iOS Local Testing
```bash
cd ios-hello-world
bundle install
bundle exec fastlane test
bundle exec fastlane build
```

### Android Local Testing
```bash
cd android-hello-world
bundle install
bundle exec fastlane test
bundle exec fastlane build_debug
```

## Troubleshooting

### Common iOS Issues
- **Code signing**: Ensure certificates are properly configured in Apple Developer portal
- **Bundle ID mismatch**: Verify bundle identifier matches in Xcode project and App Store Connect
- **Two-factor authentication**: Use app-specific passwords, not your regular Apple ID password

### Common Android Issues
- **Service account permissions**: Ensure the service account has "Release Manager" role in Google Play Console
- **Keystore issues**: Verify keystore password and alias are correct
- **API access**: Enable Google Play Developer API in Google Cloud Console

## Security Notes

- Never commit sensitive files (keystores, service account keys) to the repository
- Use GitHub Secrets for all sensitive information
- Rotate app-specific passwords and service account keys regularly
- The workflow automatically cleans up temporary files after deployment