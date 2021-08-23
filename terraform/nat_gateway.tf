# Create AWS EIP resource for NAT gateway
resource "aws_eip" "nat" {
  for_each = var.eks_public_subnet

  vpc = true

  tags = {
    "Name" = "${each.key}-${local.suffix}"
  }

  depends_on = [
    aws_internet_gateway.main
  ]
}


# Create NAT gateway from EIP
resource "aws_nat_gateway" "private" {
  for_each = var.eks_public_subnet

  allocation_id = aws_eip.nat[each.key].id
  subnet_id     = aws_subnet.eks_public[each.key].id

  tags = {
    "Name" = "${each.key}-${local.suffix}"
  }
}

# Add NAT gateway route to VPC private route table
resource "aws_route" "private" {
  for_each = var.eks_public_subnet

  route_table_id         = aws_route_table.private[each.key].id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.private[each.key].id
}
