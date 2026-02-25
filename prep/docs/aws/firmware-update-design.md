# Device Firmware Auto Update Design
Describes Device Firmware Update Functionality

I created few designs for the cloud device auto-update functionality.
- [device auto update design 1](./firmware-update-design-1.md) - simple version using just Jobs schedulingConfig feature
- [device auto update design 2](./firmware-update-design-2.md) - using EventBridge Scheduler and 2 lambdas
- [device auto update design 3](./firmware-update-design-3.md) - using EventBridge Bus and Scheduler and 3 lambdas

We decided to start with design 1 and see how it works, but create lambda the way that it can be moved to other designs, if it does not meet our requirements.
