variable "resource_group_name" {
  type        = string
  description = "Name of the resource group to create."
}

variable "name" {
  type        = string
  description = "Name of the resource group to create."
}

variable "location" {
  type        = string
  description = "Location for all resources."
}

variable "storage_account_name" {
  type        = string
  description = "Name of the storage account to create."
}

variable "environment" {
  type        = string
  description = "Environment to deploy the resources in."
}
