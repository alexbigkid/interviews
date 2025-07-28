data "aws_vpc" "default" {
  default = true
}


resource "aws_security_group" "gl-security-group" {
  vpc_id      = data.aws_vpc.default.id
  name        = "gl-security-group-${var.env}"
  description = "Allow all inbound for Postgres"
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_instance" "gl-postgre-db" {
  identifier             = "gl-postgre-db-${var.env}"
  db_name                = "glPostgreDB${var.env}"
  instance_class         = "db.t3.micro"
  allocated_storage      = 20
  engine                 = "postgres"
  engine_version         = "14.13"
  skip_final_snapshot    = true
  publicly_accessible    = true
  vpc_security_group_ids = [aws_security_group.gl-security-group.id]
  username               = var.username
  password               = var.password
}
