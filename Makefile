.PHONY:  up  down  help
up: ## Spin up containers for use mysql
	docker build -t xml-tags:v1 .
	docker run --rm xml-tags:v1

down: ## Clean all build artifacts
	docker kill xml-tags
	docker rm xml-tags

help: ## Display this help message
	@cat $(MAKEFILE_LIST) | grep -e "^[a-zA-Z_\-]*: *.*## *" | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
