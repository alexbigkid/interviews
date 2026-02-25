# AAI Agent Update
Describes AlwaysAI Agent Update

#### [back to main document](./agent-update-design.md)

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
## agent update - management API

### Example: add auto-update settings to device(s)
#### EditSettings &lambda; Request

```json
{
    "txId": "string_max_length_36",                         # Mandatory, identifies transaction
    "devices": ["device_uuid_01", "device_uuid_2", ...],    # Mandatory, devices for auto-update
    "autoUpdate": "patch" | "minor" | "major",              # Optional, auto-update type
    "autoUpdateUtcHour": 0-23,                              # Optional, if missing -> immediate update
    "autoUpdateWeekDay": 0-6                                # Optional, if missing -> daily update
}
```

#### EditSettings &lambda; Response
##### &lambda; Response, if lambda succeeds

<code>status_code: 200 (OK)</code>

```json
{
    "txId": "string_max_length_36",             # the same as txID from Lambda Request
}
```

##### &lambda; Response, if something went wrong and lambda cannot process request
<code>status_code: 403 (FORBIDDEN)</code>

```json
{
    "txId": "string_max_length_36",             # the same as txID from Lambda Request
}
```


-------------------------------------------------------------------------------
### Example: remove auto-update settings from device(s)
#### EditSettings &lambda; Request

```json
{
    "txId": "string_max_length_36",                         # Mandatory, identifies transaction
    "devices": ["device_uuid_01", "device_uuid_2", ...],    # Mandatory, device UUIDs to be removed from auto-update
}
```

#### EditSettings &lambda; Response
##### &lambda; Response, if lambda succeeds

<code>status_code: 200 (OK)</code>

```json
{
    "txId": "string_max_length_36",             # the same as txID from Lambda Request
}
```

##### &lambda; Response, if something went wrong and lambda cannot process request
<code>status_code: 403 (FORBIDDEN)</code>

```json
{
    "txId": "string_max_length_36",             # the same as txID from Lambda Request
}
```


-------------------------------------------------------------------------------
### Example: Get auto-update settings for device(s)
#### GetSettings &lambda; Request

```json
{
    "txId": "string_max_length_36",                         # Mandatory, identifies transaction
    "devices": ["device_uuid_01", "device_uuid_2", ...],    # Mandatory, devices for auto-update
}
```

#### GetSettings &lambda; Response
##### &lambda; Response, if lambda succeeds

<code>status_code: 200 (OK)</code>

```json
{
    "txId": "string_max_length_36",     # the same as txID from Lambda Request
    "devices": [
        [
            "device_uuid_01",
            "patch",                    # autoUpdate - could be patch | minor | major | null
            0,                          # autoUpdateUtcHour - could be 0-23 or null
            0                           # autoUpdateWeekDay - could be 0-6 or null
        ],
        [
            "device_uuid_02",
            "minor",                    # autoUpdate - could be patch | minor | major | null
            0,                          # autoUpdateUtcHour - could be 0-23 or null
            null                        # autoUpdateWeekDay - could be 0-6 or null
        ],
        ...
    ]
}
```

##### &lambda; Response, if something went wrong and lambda cannot process request
<code>status_code: 403 (FORBIDDEN)</code>

```json
{
    "txId": "string_max_length_36",             # the same as txID from Lambda Request
}
```


-------------------------------------------------------------------------------
### Manual Update Trigger
#### ManualTrigger &lambda; Request

```json
{
    "txId": "string_max_length_36",                         # Mandatory, identifies transaction
    "devices": ["device_uuid_01", "device_uuid_2", ...],    # Mandatory, devices for auto-update
    "autoUpdate": "patch" | "minor" | "major",              # Mandatory, update type
    "autoUpdateUtcHour": 0-23,                              # Optional, if missing -> immediate update
    "autoUpdateWeekDay": 0-6                                # Optional, if missing -> daily update
}
```

#### ManualTrigger &lambda; Response
##### &lambda; Response, if lambda succeeds

<code>status_code: 200 (OK)</code>

```json
{
    "txId": "string_max_length_36",             # the same as txID from Lambda Request
}
```


-------------------------------------------------------------------------------
### Job Creation example

The lambda would create about 168 jobs based on the update schedule (24 hours * 7 Week Days)

```json
{
  "jobId": "aai-agent-auto-update-patch-2024-10-27T23:00:00Z",
  "targets": [],
  "document": {
    "operation": "update",
    "details": {
      "applyUpdate": true
    }
  },
  "schedulingConfig": {
    "startTime": "2024-10-27T23:00:00Z",
    "timezone": "UTC"
  },
  "targetSelection": "CONTINUOUS",
  "targetType": "THING_QUERY",
  "targetQuery": {
    "sql": "SELECT * FROM AutoUpdatePatch WHERE attributes.autoUpdate = 'patch' AND attributes.autoUpdateUtcHour = '23' AND attributes.autoUpdateWeekDay = '6'"
  }
}
```
