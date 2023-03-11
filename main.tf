# Configure the Azure provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0.2"
    }
  }

  required_version = ">= 1.1.0"
}

provider "azurerm" {
  features {}
}

# Configuração para armazenar o estado do terraform

terraform {
  backend "azurerm" {
    resource_group_name  = "t10-terraform-state"
    storage_account_name = "t10terraformstate"
    container_name       = "tfstate"
    key                  = "staging.terraform.tfstate"
  }
}


# Creating a resource group

resource "azurerm_resource_group" "t10" {
  name     = "t10-resource-group"
  location = "eastus"  
  tags = {
    "env" : "staging"
    "project" : "t10-azure-challenge"
  }
}

resource "azurerm_resource_group" "t10" {
  name     = "Teste"
  location = "eastus"  
  tags = {
    "env" : "staging"
    "project" : "t10-azure-challenge"
  }
}

#teste

/*
# Criando o bucket Raw
resource "azurerm_storage_account" "raw_bucket" {
  name                     = "rawbucket"
  resource_group_name      = azurerm_resource_group.bucket_rg.name
  location                 = azurerm_resource_group.bucket_rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}


# Criando o bucket Landing
resource "azurerm_storage_account" "landing_bucket" {
  name                     = "landingbucket"
  resource_group_name      = azurerm_resource_group.bucket_rg.name
  location                 = azurerm_resource_group.bucket_rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

# Criando o bucket Curated
resource "azurerm_storage_account" "curated_bucket" {
  name                     = "curatedbucket"
  resource_group_name      = azurerm_resource_group.bucket_rg.name
  location                 = azurerm_resource_group.bucket_rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}
*/