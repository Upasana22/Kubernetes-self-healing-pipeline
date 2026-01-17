from kubernetes import client

class SelfHealingOrchestrator:
    def __init__(self):
        self.apps_v1 = client.AppsV1Api()

    def patch_deployment_resources(self, deployment_name, namespace, new_memory_limit):
        """
        Actually changes the cluster state by updating the Deployment YAML
        """
        print(f"ðŸ› ï¸  Patching {deployment_name} limits to {new_memory_limit}...")
        
        # Define the patch body
        patch_body = {
            "spec": {
                "template": {
                    "spec": {
                        "containers": [
                            {
                                "name": "stress-test", # Must match the name in your YAML
                                "resources": {
                                    "limits": {"memory": new_memory_limit},
                                    "requests": {"memory": new_memory_limit}
                                }
                            }
                        ]
                    }
                }
            }
        }

        try:
            # apps_v1 is an instance of client.AppsV1Api()
            self.apps_v1.patch_namespaced_deployment(
                name=deployment_name,
                namespace=namespace,
                body=patch_body
            )
            print("âœ… Patch successful! Deployment is restarting with more resources.")
        except Exception as e:
            print(f"âŒ Failed to patch: {e}")

# Usage Example
# orchestrator = SelfHealingOrchestrator()
# orchestrator.patch_deployment_resources("memory-leaker", "default", "256Mi")
