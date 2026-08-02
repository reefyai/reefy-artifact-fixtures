// SPDX-License-Identifier: MIT
#include <linux/init.h>
#include <linux/module.h>

static int __init reefy_e2e_artifact_init(void)
{
	pr_info("reefy_e2e_artifact: synthetic E2E module loaded\n");
	return 0;
}

static void __exit reefy_e2e_artifact_exit(void)
{
	pr_info("reefy_e2e_artifact: synthetic E2E module unloaded\n");
}

module_init(reefy_e2e_artifact_init);
module_exit(reefy_e2e_artifact_exit);

MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Harmless Reefy OCI artifact E2E fixture");
