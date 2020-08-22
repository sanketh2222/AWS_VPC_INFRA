from aws_cdk import core
from aws_cdk import aws_ec2 as _ec2
from aws_cdk import aws_apigateway as _apig
from aws_cdk import aws_cloudwatch as _cw
from aws_cdk import aws_sns as _sns
from aws_cdk import aws_sns_subscriptions as _subs
from aws_cdk import aws_logs as _logs
from aws_cdk import aws_cloudwatch_actions as _cwact
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_iam as _iam



import json
import os


class LiveDashboardStack(core.Stack):
    
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        try:
            with open("serverless_stack/lambda_codes/log_generator.py",mode="r") as f:
                lambda_code=f.read()
                print("file read\n")
        except OSError:
            print("file not found")
        
        
        log_fn=_lambda.Function(
            self,
            "lambdafn",
            # code=_lambda.InlineCode(lambda_code),
            code=_lambda.Code.from_inline(lambda_code),
            handler="index.lambda_handler",
            runtime=_lambda.Runtime.PYTHON_3_7,
            environment={
                "var":"1",# not able to set integer values 
                "LOG_LEVEL": "INFO",# CREATES ENVIRONMENT VARIABLES
                "Percentage_error":"90"
            },
            reserved_concurrent_executions=1,
            timeout=core.Duration.seconds(3),
            function_name="Metric_Filter"
        )
        
        
        # Create Custom Loggroup
        # /aws/lambda/function-name
        custom_metric_lg = _logs.LogGroup(self,
                                                   "konstoneLoggroup",
                                                   log_group_name=f"/aws/lambda/{log_fn.function_name}",
                                                   removal_policy=core.RemovalPolicy.DESTROY,
                                                   retention=_logs.RetentionDays.ONE_DAY,
                                                   )
        
        # creating namespace for 3rd party metric
        
        third_party_metric= _cw.Metric(
            metric_name="Third_party_metric",
            namespace="Third_party_metric_namespace",
            statistic="sum",
            period=core.Duration.minutes(1)
        )
        
        # filter metric
        third_party_metric_filter=_logs.MetricFilter(
            self,
            "metricfilter",
            log_group =custom_metric_lg,
            filter_pattern =_logs.FilterPattern.boolean_value(
                "$.third_party_api_error",True
            ),
            metric_name =third_party_metric.metric_name,
            metric_namespace =third_party_metric.namespace,
            default_value =0,
            metric_value ="1"
        )
        
        # creating alarm
        fn_alarm=_cw.Alarm(
            self,
            "filtermetricalarm",
            metric=third_party_metric,
            evaluation_periods =2,
            alarm_description ="Alert if 3rd party API has more than 2 errors in the last two minutes",
            alarm_name ="Custom_metic_filter",
            threshold=2,
            comparison_operator =_cw.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            datapoints_to_alarm =1,
            period=core.Duration.minutes(1),
            treat_missing_data=_cw.TreatMissingData.NOT_BREACHING
        )
        
        # creating dashboard
        dashboard=_cw.Dashboard(
            self,
            "dashboard",
            dashboard_name ="My_Dashboard"
        )
        
        dashboard.add_widgets(
            _cw.Row(
                _cw.GraphWidget(
                left=[
                    log_fn.metric_invocations(
                        statistic="sum",
                        period=core.Duration.minutes(1)
                    )
                ],
                title="Invocation Graph"
                ),
                _cw.GraphWidget(
                    left=[log_fn.metric_errors(
                        period=core.Duration.minutes(1)
                    )],
                    title="Error Graph"
                )
            )
        )
        
        dashboard.add_widgets(
            _cw.Row(
                _cw.SingleValueWidget(
                    metrics=[third_party_metric],
                    title="Filter Metic"
                )
            )
        )