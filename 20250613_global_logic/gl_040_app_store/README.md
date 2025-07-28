# Mobile App CI/CD Pipeline

This repository demonstrates a professional mobile CI/CD pipeline for iOS and Android applications using GitHub Actions and Fastlane. The pipeline follows DevOps best practices with separated build and deployment stages, quality gates, and artifact promotion.

## 📱 Apps Overview

- **iOS Hello World App**: Located in `ios-hello-world/`
- **Android Hello World App**: Located in `android-hello-world/`
- **Automated Deployment**: Using Fastlane and GitHub Actions
- **Store Deployment**: TestFlight/App Store (iOS) and Google Play Store (Android)

## 🏗️ CI/CD Architecture Overview

```mermaid
graph TB
    subgraph "Developer Workflow"
        A[👨‍💻 Developer Push] --> B{Code Change?}
        B -->|Yes| C[🧪 Run Tests]
        B -->|Release Tag| D[🏷️ Release Tag Push]
    end
    
    subgraph "CI Pipeline (Always)"
        C --> E[✅ Unit Tests]
        E --> F[📦 Build Debug]
        F --> G[📤 Upload Test Results]
    end
    
    subgraph "CD Pipeline (On Tags Only)"
        D --> H{Tests Pass?}
        H -->|✅ Yes| I[🔢 Version Bump]
        H -->|❌ No| J[🛑 Stop Pipeline]
        I --> K[🔐 Code Signing]
        K --> L[📱 Build Release]
        L --> M[🚀 Deploy to Beta]
        M --> N[📦 Store Artifacts]
        N --> O[🏷️ Create Version Tag]
    end
    
    subgraph "Production Deploy (Manual Trigger)"
        P[👤 Manual Trigger] --> Q[📥 Download Artifacts]
        Q --> R[🏪 Auto Deploy to Production]
    end
    
    N -.-> P
    
    style E fill:#90EE90
    style H fill:#FFB6C1
    style M fill:#87CEEB
    style R fill:#FFA500
```

## 📊 iOS Pipeline Detailed Flow

```mermaid
flowchart TD
    subgraph "Trigger Events"
        A1[📝 Push to main/develop] 
        A2[🔀 Pull Request]
        A3[🏷️ ios-patch tag]
        A4[🏷️ ios-minor tag] 
        A5[🏷️ ios-major tag]
        A6[👤 Manual Trigger]
    end
    
    subgraph "Test Job (Always Runs)"
        B1[🔧 Setup macOS + Xcode]
        B2[💎 Setup Ruby + Fastlane]
        B3[🧪 Run Unit Tests]
        B4[🔨 Build for Testing]
        B5[📤 Upload Test Results]
    end
    
    subgraph "Release Job (Tags Only + Tests Pass)"
        C1{🏷️ Release Tag?}
        C2[🔐 Install Certificates]
        C3[📋 Setup Provisioning Profiles]
        C4[🔢 Version Bump Logic]
        C5[📱 Build Release IPA]
        C6[🚀 Deploy to TestFlight]
        C7[📦 Store Build Artifacts]
        C8[📝 Commit Version Changes]
        C9[🏷️ Create Version Tag<br/>v1.2.3-ios]
    end
    
    subgraph "Production Deploy (Manual Trigger)"
        D1[👤 Manual Trigger via GitHub UI]
        D2[📥 Auto Download Artifacts]
        D3[🏪 Auto Deploy to App Store]
        D4[📋 Production Review Required]
    end
    
    A1 --> B1
    A2 --> B1
    A3 --> B1
    A4 --> B1
    A5 --> B1
    A6 --> B1
    
    B1 --> B2 --> B3 --> B4 --> B5
    
    B5 --> C1
    C1 -->|✅ Yes + Tests Pass| C2
    C1 -->|❌ No| E[⏹️ End]
    
    C2 --> C3 --> C4 --> C5 --> C6 --> C7 --> C8 --> C9
    
    C7 -.->|Artifact Available| D1
    D1 --> D2 --> D3 --> D4
    
    style B3 fill:#90EE90
    style C1 fill:#FFB6C1
    style C6 fill:#87CEEB
    style D3 fill:#FFA500
```

## 🤖 Android Pipeline Detailed Flow

```mermaid
flowchart TD
    subgraph "Trigger Events"
        A1[📝 Push to main/develop]
        A2[🔀 Pull Request]
        A3[🏷️ android-patch tag]
        A4[🏷️ android-minor tag]
        A5[🏷️ android-major tag]
        A6[👤 Manual Trigger]
    end
    
    subgraph "Test Job (Always Runs)"
        B1[🔧 Setup Ubuntu + Java]
        B2[🤖 Setup Android SDK]
        B3[💎 Setup Ruby + Fastlane]
        B4[🧪 Run Unit Tests]
        B5[🔨 Build Debug APK]
        B6[📤 Upload Test Results]
    end
    
    subgraph "Release Job (Tags Only + Tests Pass)"
        C1{🏷️ Release Tag?}
        C2[🔐 Setup Keystore]
        C3[🔑 Setup Service Account]
        C4[🔢 Version Bump Logic]
        C5[📱 Build Release AAB]
        C6[🚀 Deploy to Play Beta]
        C7[📦 Store Build Artifacts]
        C8[📝 Commit Version Changes]
        C9[🏷️ Create Version Tag<br/>v1.2.3-android]
        C10[🧹 Cleanup Credentials]
    end
    
    subgraph "Production Deploy (Manual Trigger)"
        D1[👤 Manual Trigger via GitHub UI]
        D2[📥 Auto Download Artifacts]
        D3[🏪 Auto Deploy to Play Store]
        D4[📋 Track Selection]
        D5[🎯 Internal/Alpha/Beta/Prod]
    end
    
    A1 --> B1
    A2 --> B1
    A3 --> B1
    A4 --> B1
    A5 --> B1
    A6 --> B1
    
    B1 --> B2 --> B3 --> B4 --> B5 --> B6
    
    B6 --> C1
    C1 -->|✅ Yes + Tests Pass| C2
    C1 -->|❌ No| E[⏹️ End]
    
    C2 --> C3 --> C4 --> C5 --> C6 --> C7 --> C8 --> C9 --> C10
    
    C7 -.->|Artifact Available| D1
    D1 --> D2 --> D3 --> D4 --> D5
    
    style B4 fill:#90EE90
    style C1 fill:#FFB6C1
    style C6 fill:#87CEEB
    style D3 fill:#FFA500
```

## 🔐 Binary Signing & Security

### iOS Code Signing

```mermaid
graph LR
    subgraph "Apple Developer Portal"
        A[🎫 Developer Certificate]
        B[📋 Provisioning Profile]
        C[🆔 App ID]
    end
    
    subgraph "Fastlane Match"
        D[🔐 Certificate Storage]
        E[☁️ Cloud Storage/Git]
        F[🔑 Match Password]
    end
    
    subgraph "Build Process"
        G[📱 Xcode Project]
        H[✍️ Code Signing]
        I[📦 Signed IPA]
    end
    
    A --> D
    B --> D
    C --> D
    D --> E
    F --> E
    E --> H
    G --> H
    H --> I
    
    style A fill:#FFE4E1
    style H fill:#90EE90
    style I fill:#87CEEB
```

**iOS Signing Files Location:**
- **Certificates**: Managed by Fastlane Match (stored in cloud/git)
- **Provisioning Profiles**: Downloaded automatically during build
- **Configuration**: `ios-hello-world/fastlane/Matchfile` (if using Match)

**Platform Requirements:**
- **Building iOS Apps**: Requires macOS + Xcode (cannot be done on Linux)
- **Deploying Pre-built IPAs**: Can be done from Linux using:
  - Fastlane's `upload_to_app_store` action
  - App Store Connect API
  - Apple's Transporter tool (now available on Linux)

### Android Code Signing

```mermaid
graph LR
    subgraph "Google Play Console"
        A[🔑 Service Account]
        B[📜 JSON Key File]
        C[🎯 App Bundle ID]
    end
    
    subgraph "Android Keystore"
        D[🗝️ Keystore File]
        E[🔐 Keystore Password]
        F[🏷️ Key Alias]
        G[🔑 Key Password]
    end
    
    subgraph "Build Process"
        H[🤖 Gradle Build]
        I[✍️ APK/AAB Signing]
        J[📦 Signed AAB]
    end
    
    A --> B
    D --> I
    E --> I
    F --> I
    G --> I
    H --> I
    I --> J
    
    style D fill:#FFE4E1
    style I fill:#90EE90
    style J fill:#87CEEB
```

**Android Signing Files Location:**
- **Keystore**: `android-keystore.jks` (created during build from base64 secret)
- **Service Account**: `google-play-service-account.json` (created during build)
- **Configuration**: `android-hello-world/app/build.gradle` (signing config)

## 📸 Screenshots & App Store Assets

### iOS App Store Connect

Screenshots and metadata are managed in App Store Connect:

```mermaid
graph TB
    subgraph "App Store Connect"
        A[📱 App Store Connect Portal]
        B[🖼️ Screenshots<br/>Various Device Sizes]
        C[📝 App Description]
        D[🏷️ Keywords & Categories]
        E[🎬 App Preview Videos]
        F[📋 App Review Information]
    end
    
    subgraph "Required Screenshot Sizes"
        G[📱 iPhone 6.7 inch]
        H[📱 iPhone 6.5 inch]
        I[📱 iPhone 5.5 inch]
        J[📱 iPad Pro 12.9 inch]
        K[📱 iPad Pro 11 inch]
    end
    
    A --> B
    A --> C
    A --> D
    A --> E
    A --> F
    
    B --> G
    B --> H
    B --> I
    B --> J
    B --> K
    
    style A fill:#87CEEB
    style B fill:#FFB6C1
```

**iOS Assets Location:**
- **Portal**: [App Store Connect](https://appstoreconnect.apple.com)
- **Screenshots**: Upload manually through web interface
- **Metadata**: Managed through App Store Connect or Fastlane's `deliver`

### Android Google Play Console

```mermaid
graph TB
    subgraph "Google Play Console"
        A[🤖 Google Play Console]
        B[🖼️ Phone Screenshots]
        C[📱 Tablet Screenshots]
        D[📺 TV Screenshots]
        E[⌚ Wear Screenshots]
        F[📝 Store Listing]
        G[🎬 Feature Graphic]
    end
    
    subgraph "Screenshot Requirements"
        H[📱 Phone: 16:9 or 9:16]
        I[📱 Tablet: 16:10, 16:9, 3:2]
        J[📺 TV: 16:9]
        K[⌚ Wear: Square]
    end
    
    A --> B
    A --> C
    A --> D
    A --> E
    A --> F
    A --> G
    
    B --> H
    C --> I
    D --> J
    E --> K
    
    style A fill:#87CEEB
    style F fill:#FFB6C1
```

**Android Assets Location:**
- **Portal**: [Google Play Console](https://play.google.com/console)
- **Screenshots**: Upload through web interface
- **Metadata**: Managed through Play Console or Fastlane's `supply`

## 🚀 Developer Workflow Examples

### Quick Development Test

```bash
# Regular development - tests always run
git add .
git commit -m "Fix login bug"
git push origin develop

# ✅ Tests run automatically
# ✅ Build verification
# ❌ No deployment (no release tag)
```

### iOS Release Deployment

```bash
# Create iOS release
git checkout main
git pull origin main
git tag ios-patch          # or ios-minor, ios-major
git push origin ios-patch

# ✅ Tests run first
# ✅ Version bump: 1.0.0 → 1.0.1
# ✅ Build signed IPA
# ✅ Deploy to TestFlight
# ✅ Create version tag: v1.0.1-ios
# ✅ Store artifacts for production
```

### Android Release Deployment

```bash
# Create Android release  
git checkout main
git pull origin main
git tag android-minor       # or android-patch, android-major
git push origin android-minor

# ✅ Tests run first
# ✅ Version bump: 1.0.0 → 1.1.0
# ✅ Build signed AAB
# ✅ Deploy to Play Store Beta
# ✅ Create version tag: v1.1.0-android
# ✅ Store artifacts for production
```

### Production Deployment (Manual Trigger, Automated Execution)

**Manual Steps (Developer Action):**
1. **Go to GitHub Actions**
2. **Select deployment workflow:**
   - `iOS Deploy to App Store`
   - `Android Deploy to Play Store`
3. **Click "Run workflow"**
4. **Enter build number** (from previous build)
5. **Select environment:**
   - iOS: `testflight` or `production`
   - Android: `internal`, `alpha`, `beta`, or `production`
6. **Click "Run workflow"**

**Automated Steps (Pipeline Execution):**
- ✅ Downloads artifacts automatically
- ✅ Sets up signing certificates automatically
- ✅ Deploys to selected store/track automatically
- ✅ Handles all deployment steps without intervention

## 📁 Project Structure

```
📦 Mobile-App-CI-CD/
├── 📱 ios-hello-world/
│   ├── 🎯 HelloWorld.xcodeproj/        # Xcode project
│   ├── 📁 HelloWorld/                  # iOS source code
│   ├── 🚀 fastlane/                   # iOS deployment scripts
│   │   ├── Fastfile                   # Fastlane actions
│   │   └── Appfile                    # App configuration
│   └── 💎 Gemfile                     # Ruby dependencies
├── 🤖 android-hello-world/
│   ├── 📁 app/                        # Android source code
│   │   ├── build.gradle               # App build configuration
│   │   └── src/main/                  # Source files
│   ├── 🚀 fastlane/                   # Android deployment scripts
│   │   ├── Fastfile                   # Fastlane actions
│   │   └── Appfile                    # App configuration
│   ├── 🔧 build.gradle                # Project build configuration
│   └── 💎 Gemfile                     # Ruby dependencies
├── ⚙️ .github/workflows/              # CI/CD pipelines
│   ├── ios-build.yml                 # iOS build & test
│   ├── ios-deploy.yml                # iOS production deploy
│   ├── android-build.yml             # Android build & test
│   └── android-deploy.yml            # Android production deploy
├── 🔐 .envrc                         # Environment variables
├── 📖 README.md                      # This file
└── 📋 DEPLOYMENT.md                  # Detailed deployment guide
```

## 🎯 Key Benefits for DevOps

- **✅ Quality Gates**: Tests must pass before any deployment
- **🔄 Artifact Promotion**: Build once, deploy multiple times
- **🎯 Environment Separation**: Clear staging → production flow  
- **🔐 Security**: Credential management with auto-cleanup
- **📊 Audit Trail**: Version tags track every release
- **⚡ Fast Feedback**: Quick test results on every push
- **🛡️ Safe Deployments**: Manual approval for production
- **📈 Scalable**: Easy to add new environments or features

## 🖥️ Platform Considerations

### iOS Deployment Options

**Current Pipeline (macOS-based):**
- ✅ **Build + Deploy**: Complete pipeline on macOS runners
- ✅ **Full Integration**: Xcode, signing, TestFlight in one workflow

**Alternative: Linux-based Deployment** (for pre-built IPAs):
```yaml
# Example: Deploy pre-built iOS app from Linux
- name: Deploy to App Store (Linux)
  uses: apple-actions/upload-to-app-store@v1
  with:
    ipa-path: ./artifacts/app.ipa
    api-key: ${{ secrets.APP_STORE_CONNECT_API_KEY }}
```

**Trade-offs:**
- **macOS Runners**: More expensive but complete iOS toolchain
- **Linux Runners**: Cheaper but requires pre-built artifacts
- **Hybrid Approach**: Build on macOS, deploy from Linux (advanced setup)

### Android Deployment
- ✅ **Full Linux Support**: Complete build and deployment pipeline
- ✅ **Cost Effective**: Standard GitHub runners
- ✅ **Fast Execution**: No platform limitations

## 📚 Documentation

- **[DEPLOYMENT.md](DEPLOYMENT.md)**: Complete deployment setup guide
- **[GitHub Secrets Setup](DEPLOYMENT.md#github-secrets-configuration)**: Required secrets configuration
- **[Local Development](DEPLOYMENT.md#local-development)**: Local testing instructions
- **[Fastlane Documentation](https://docs.fastlane.tools/)**: Official Fastlane documentation and guides

---

**Perfect for DevOps interviews!** This pipeline demonstrates enterprise-level CI/CD practices with proper gates, security, and auditability.