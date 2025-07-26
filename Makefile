# Neo4j Container Management Makefile
# Provides easy commands to manage the Neo4j database container

# Configuration
CONTAINER_NAME := c2s-neo4j
NEO4J_URL := http://localhost:7474
NEO4J_BOLT_URL := bolt://localhost:7687
NEO4J_USER := neo4j
NEO4J_PASSWORD := password123
BACKUP_DIR := ./backups
TIMESTAMP := $(shell date +%Y%m%d_%H%M%S)

# Colors for output
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
BLUE := \033[0;34m
NC := \033[0m

# Default target
.DEFAULT_GOAL := help

# Check if Docker is running
.PHONY: check-docker
check-docker:
	@if ! docker info > /dev/null 2>&1; then \
		echo "$(RED)[ERROR]$(NC) Docker is not running. Please start Docker first."; \
		exit 1; \
	fi

# Start Neo4j database
.PHONY: start
start: check-docker
	@echo "$(BLUE)[Neo4j Manager]$(NC) Starting Neo4j database..."
	@if docker ps -q -f name=$(CONTAINER_NAME) | grep -q .; then \
		echo "$(YELLOW)[WARNING]$(NC) Neo4j container is already running"; \
	else \
		docker-compose up -d neo4j; \
		echo "$(GREEN)[INFO]$(NC) Neo4j started successfully"; \
		echo "$(GREEN)[INFO]$(NC) Web interface: $(NEO4J_URL)"; \
		echo "$(GREEN)[INFO]$(NC) Bolt connection: $(NEO4J_BOLT_URL)"; \
		echo "$(GREEN)[INFO]$(NC) Username: $(NEO4J_USER)"; \
		echo "$(GREEN)[INFO]$(NC) Password: $(NEO4J_PASSWORD)"; \
	fi

# Stop Neo4j database
.PHONY: stop
stop: check-docker
	@echo "$(BLUE)[Neo4j Manager]$(NC) Stopping Neo4j database..."
	@if docker ps -q -f name=$(CONTAINER_NAME) | grep -q .; then \
		docker-compose down; \
		echo "$(GREEN)[INFO]$(NC) Neo4j stopped successfully"; \
	else \
		echo "$(YELLOW)[WARNING]$(NC) Neo4j container is not running"; \
	fi

# Restart Neo4j database
.PHONY: restart
restart: stop
	@sleep 2
	@$(MAKE) start

# Check Neo4j status
.PHONY: status
status: check-docker
	@echo "$(BLUE)[Neo4j Manager]$(NC) Checking Neo4j status..."
	@if docker ps -q -f name=$(CONTAINER_NAME) | grep -q .; then \
		echo "$(GREEN)[INFO]$(NC) Neo4j container is running"; \
		echo ""; \
		echo "Container details:"; \
		docker ps --filter name=$(CONTAINER_NAME) --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"; \
		echo ""; \
		if curl -s -f $(NEO4J_URL) > /dev/null 2>&1; then \
			echo "$(GREEN)[INFO]$(NC) Neo4j web interface is accessible at $(NEO4J_URL)"; \
		else \
			echo "$(YELLOW)[WARNING]$(NC) Neo4j web interface is not responding yet (may still be starting up)"; \
		fi \
	else \
		echo "$(YELLOW)[WARNING]$(NC) Neo4j container is not running"; \
	fi

# View Neo4j logs
.PHONY: logs
logs: check-docker
	@echo "$(BLUE)[Neo4j Manager]$(NC) Viewing Neo4j logs..."
	@if docker ps -q -f name=$(CONTAINER_NAME) | grep -q .; then \
		docker logs -f $(CONTAINER_NAME); \
	else \
		echo "$(RED)[ERROR]$(NC) Neo4j container is not running"; \
		exit 1; \
	fi

# Open Neo4j Cypher shell
.PHONY: shell
shell: check-docker
	@echo "$(BLUE)[Neo4j Manager]$(NC) Opening Neo4j shell..."
	@if docker ps -q -f name=$(CONTAINER_NAME) | grep -q .; then \
		echo "$(GREEN)[INFO]$(NC) Connecting to Neo4j shell..."; \
		docker exec -it $(CONTAINER_NAME) cypher-shell -u $(NEO4J_USER) -p $(NEO4J_PASSWORD); \
	else \
		echo "$(RED)[ERROR]$(NC) Neo4j container is not running"; \
		exit 1; \
	fi

# Reset Neo4j database (delete all data)
.PHONY: reset
reset:
	@echo "$(BLUE)[Neo4j Manager]$(NC) Resetting Neo4j database..."
	@echo "$(YELLOW)[WARNING]$(NC) This will delete ALL data in the Neo4j database!"
	@read -p "Are you sure you want to continue? (y/N): " confirm && \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		$(MAKE) stop; \
		docker volume rm c2s-dspy_neo4j_data 2>/dev/null || true; \
		docker volume rm c2s-dspy_neo4j_logs 2>/dev/null || true; \
		echo "$(GREEN)[INFO]$(NC) Neo4j data volumes removed"; \
		$(MAKE) start; \
	else \
		echo "$(GREEN)[INFO]$(NC) Reset cancelled"; \
	fi

# Create backup directory
$(BACKUP_DIR):
	@mkdir -p $(BACKUP_DIR)

# Backup Neo4j database
.PHONY: backup
backup: check-docker $(BACKUP_DIR)
	@echo "$(BLUE)[Neo4j Manager]$(NC) Creating Neo4j backup..."
	@if ! docker ps -q -f name=$(CONTAINER_NAME) | grep -q .; then \
		echo "$(RED)[ERROR]$(NC) Neo4j container is not running"; \
		exit 1; \
	fi
	@BACKUP_FILE="neo4j_backup_$(TIMESTAMP).dump"; \
	echo "$(GREEN)[INFO]$(NC) Creating backup: $$BACKUP_FILE"; \
	docker exec $(CONTAINER_NAME) neo4j-admin database dump --to-path=/tmp neo4j; \
	docker cp $(CONTAINER_NAME):/tmp/neo4j.dump $(BACKUP_DIR)/$$BACKUP_FILE; \
	echo "$(GREEN)[INFO]$(NC) Backup created successfully: $(BACKUP_DIR)/$$BACKUP_FILE"

# List available backups
.PHONY: list-backups
list-backups:
	@echo "$(BLUE)[Neo4j Manager]$(NC) Available backups:"
	@if [ -d "$(BACKUP_DIR)" ] && [ -n "$$(ls -A $(BACKUP_DIR) 2>/dev/null)" ]; then \
		ls -la $(BACKUP_DIR)/*.dump 2>/dev/null || echo "No backup files found"; \
	else \
		echo "No backup directory or files found"; \
	fi

# Restore from backup (requires BACKUP_FILE parameter)
.PHONY: restore
restore: check-docker
	@if [ -z "$(BACKUP_FILE)" ]; then \
		echo "$(RED)[ERROR]$(NC) Please specify BACKUP_FILE parameter"; \
		echo "Usage: make restore BACKUP_FILE=backup_filename.dump"; \
		echo "Available backups:"; \
		$(MAKE) list-backups; \
		exit 1; \
	fi
	@if [ ! -f "$(BACKUP_DIR)/$(BACKUP_FILE)" ]; then \
		echo "$(RED)[ERROR]$(NC) Backup file $(BACKUP_DIR)/$(BACKUP_FILE) not found"; \
		exit 1; \
	fi
	@echo "$(BLUE)[Neo4j Manager]$(NC) Restoring from backup: $(BACKUP_FILE)"
	@echo "$(YELLOW)[WARNING]$(NC) This will replace ALL current data!"
	@read -p "Are you sure you want to continue? (y/N): " confirm && \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		$(MAKE) stop; \
		docker volume rm c2s-dspy_neo4j_data 2>/dev/null || true; \
		$(MAKE) start; \
		sleep 10; \
		$(MAKE) stop; \
		docker cp $(BACKUP_DIR)/$(BACKUP_FILE) $(CONTAINER_NAME):/tmp/restore.dump; \
		docker exec $(CONTAINER_NAME) neo4j-admin database load --from-path=/tmp neo4j --overwrite-destination=true; \
		$(MAKE) start; \
		echo "$(GREEN)[INFO]$(NC) Restore completed successfully"; \
	else \
		echo "$(GREEN)[INFO]$(NC) Restore cancelled"; \
	fi

# Clean up stopped containers and unused volumes
.PHONY: clean
clean: check-docker
	@echo "$(BLUE)[Neo4j Manager]$(NC) Cleaning up Docker resources..."
	@docker container prune -f
	@docker volume prune -f
	@echo "$(GREEN)[INFO]$(NC) Cleanup completed"

# Pull latest Neo4j image
.PHONY: update
update: check-docker
	@echo "$(BLUE)[Neo4j Manager]$(NC) Updating Neo4j image..."
	@docker-compose pull neo4j
	@echo "$(GREEN)[INFO]$(NC) Neo4j image updated. Run 'make restart' to use the new image"

# Show connection information
.PHONY: info
info:
	@echo "$(BLUE)[Neo4j Connection Information]$(NC)"
	@echo "Web Interface: $(NEO4J_URL)"
	@echo "Bolt Connection: $(NEO4J_BOLT_URL)"
	@echo "Username: $(NEO4J_USER)"
	@echo "Password: $(NEO4J_PASSWORD)"
	@echo "Container Name: $(CONTAINER_NAME)"

# Open Neo4j web interface in browser (macOS/Linux)
.PHONY: web
web:
	@echo "$(GREEN)[INFO]$(NC) Opening Neo4j web interface..."
	@if command -v open >/dev/null 2>&1; then \
		open $(NEO4J_URL); \
	elif command -v xdg-open >/dev/null 2>&1; then \
		xdg-open $(NEO4J_URL); \
	else \
		echo "$(YELLOW)[WARNING]$(NC) Could not open browser automatically"; \
		echo "Please open $(NEO4J_URL) in your browser"; \
	fi

# Show help
.PHONY: help
help:
	@echo "Neo4j Database Manager"
	@echo ""
	@echo "Usage: make [TARGET]"
	@echo ""
	@echo "Targets:"
	@echo "  start          Start Neo4j database"
	@echo "  stop           Stop Neo4j database"
	@echo "  restart        Restart Neo4j database"
	@echo "  status         Show Neo4j status"
	@echo "  logs           View Neo4j logs (follow mode)"
	@echo "  shell          Open Neo4j Cypher shell"
	@echo "  reset          Reset Neo4j database (delete all data)"
	@echo "  backup         Create a backup of Neo4j database"
	@echo "  restore        Restore from backup (requires BACKUP_FILE parameter)"
	@echo "  list-backups   List available backup files"
	@echo "  clean          Clean up stopped containers and unused volumes"
	@echo "  update         Pull latest Neo4j image"
	@echo "  info           Show connection information"
	@echo "  web            Open Neo4j web interface in browser"
	@echo "  help           Show this help message"
	@echo ""
	@echo "Examples:"
	@echo "  make start                                    # Start Neo4j"
	@echo "  make status                                   # Check if Neo4j is running"
	@echo "  make shell                                    # Open Cypher shell for queries"
	@echo "  make backup                                   # Create a backup"
	@echo "  make restore BACKUP_FILE=neo4j_backup_20231201_143022.dump  # Restore from backup"
	@echo ""
	@echo "Connection Details:"
	@echo "  Web Interface: $(NEO4J_URL)"
	@echo "  Bolt Connection: $(NEO4J_BOLT_URL)"
	@echo "  Username: $(NEO4J_USER)"
	@echo "  Password: $(NEO4J_PASSWORD)"
