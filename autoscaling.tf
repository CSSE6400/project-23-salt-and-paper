# Code mostly taken from [3]
resource "aws_appautoscaling_target" "saltandpaper_autoscaling" { 
  max_capacity        = 4 
  min_capacity        = 1 
  resource_id         = "service/${aws_ecs_service.saltandpaper_ecs.name}/${aws_ecs_cluster.saltandpaper.name}"
  scalable_dimension  = "ecs:service:DesiredCount" 
  service_namespace   = "ecs" 
} 
 
 
resource "aws_appautoscaling_policy" "saltandpaper-cpu" { 
  name                = "saltandpaper-cpu" 
  policy_type         = "TargetTrackingScaling" 
  resource_id         = aws_appautoscaling_target.saltandpaper_autoscaling.resource_id 
  scalable_dimension  = aws_appautoscaling_target.saltandpaper_autoscaling.scalable_dimension 
  service_namespace   = aws_appautoscaling_target.saltandpaper_autoscaling.service_namespace 
 
  target_tracking_scaling_policy_configuration { 
    predefined_metric_specification { 
      predefined_metric_type  = "ECSServiceAverageCPUUtilization" 
    } 
 
    target_value              = 20 
  } 
}