# Firmware Update
Describes Device Firmware Update

#### [back to main document](./firmware-update-design.md)
#### [view lambda interface](./firmware-update-lambda-io.md)

[TOC]

## Agent Update Requirements.
Instead of creating a typical Req/Resp RESTful API to update our devices, we should create an event driven update strategy to satisfy all requirements for agent updates.
Here are the requirements:

- set devices to auto-update
- hold off updates
- update devices as soon as update becomes available
- update only patch versions: bug fixes, security fixes
- update only minor versions: patch + features with backwards compatibility
- update major versions: all updates
- possibility to update at specific time
- possibility to do blue/green update rollout
- possibility to rollback an update
- possibility update group of devices as well as individual devices


-------------------------------------------------------------------------------
## Event driven design 1
### Overview

```mermaid
graph LR
    subgraph Color Legend
        pipeline(CI/CD pipeline)
        s3(S3)
        iot_core(IoT Core)
        lambda(Lambda)
        device_firmware(device-firmware)
    end

    classDef PIPELINE fill:#3498db,stroke:#333,stroke-width:2px
    classDef S3 fill:#f6d743,stroke:#333,stroke-width:2px
    classDef IOT_CORE fill:#ffc0cb,stroke:#333,stroke-width:2px
    classDef LAMBDA fill:#9f6,stroke:#333,stroke-width:2px
    classDef device_firmware fill:#,stroke:#333,stroke-width:2px

    class pipeline PIPELINE
    class s3 S3
    class iot_core IOT_CORE
    class lambda LAMBDA
    class device_firmware DEVICE_FIRMWARE
```

```mermaid
graph LR
    subgraph AWS
        s3(S3 device-firmware<br>release bucket) --> s3_lambda(S3 triggered &lambda;)
        s3_lambda --> iot_core_tg(IoT Core<br>Thing Groups)
        iot_core_tg --> |auto-update<br>groups| s3_lambda
        s3_lambda --> |immediate<br>jobs| iot_core_jobs(IoT Core<br>Jobs)
        s3_lambda --> |scheduled<br>jobs| iot_core_jobs
    end
    pipeline(CI/CD<br>pipeline) --> |compiled<br>binaries| s3
    iot_core_jobs --> |update| device_firmware(device-firmware)

    classDef PIPELINE fill:#3498db,stroke:#333,stroke-width:2px
    classDef BAD_BAD_EVENT fill:#f00,color:white,font-weight:bold,stroke-width:2px,stroke:yellow
    classDef S3 fill:#f6d743,stroke:#333,stroke-width:2px
    classDef IOT_CORE fill:#ffc0cb,stroke:#333,stroke-width:2px
    classDef EVENT_BRIDGE fill:#f96,stroke:#333,stroke-width:2px;
    classDef LAMBDA fill:#9f6,stroke:#333,stroke-width:2px

    class pipeline PIPELINE
    class dlq BAD_BAD_EVENT
    class s3 S3
    class iot_core_tg IOT_CORE
    class iot_core_jobs IOT_CORE
    class iot_core_jobs IOT_CORE
    class event_bridge EVENT_BRIDGE
    class s3_lambda LAMBDA
    class scheduled_lambda LAMBDA
```

### device-firmware update Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    participant pipeline as CI/CD<br>pipeline
    participant s3_versions as S3 releases<br>for device-firmware
    participant s3_lambda as S3 triggered<br>Lambda
    participant iot_core_tg as IoT Core<br>Thing Groups
    participant iot_core_jobs as IoT Core<br>Jobs
    participant device_firmware as Device Firmware

    rect rgb(89, 255, 89)
        Note over s3_versions,iot_core_jobs: AWS
    end

    pipeline->>s3_versions: store new binary<br>version for device-firmware
    s3_versions->>s3_lambda: update available

    s3_lambda->>iot_core_tg: get groups<br>for auto-update
    iot_core_tg-->>s3_lambda: thing groups<br>to auto-update
    s3_lambda->>iot_core_jobs: create jobs for immediate update
    iot_core_jobs->>device_firmware: update device-firmware version

    s3_lambda->>iot_core_jobs: create jobs<br>for scheduled update
    iot_core_jobs->>device_firmware: update device-firmware version

```
