# Reefy artifact fixtures

Synthetic, signed OCI host-extension artifacts used only by Reefy's end-to-end
test suite. Payloads are bound to an exact Reefy build ID and kernel ABI. The
activation hook loads a harmless out-of-tree test module, writes a runtime
marker, and publishes a synthetic CDI device.
