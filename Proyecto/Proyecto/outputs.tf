output "instance_id" {
    description = "ID de instancia EC2"
    value       = aws_instance.Examen3.id

}

output "instance_public_ip" {
    description = "IP publica de instancia EC2"
    value       = aws_instance.Examen3.public_ip

}