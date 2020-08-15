from aws_cdk import aws_secretsmanager as  _secretmanager
from aws_cdk import aws_ssm as _ssm
from aws_cdk import core
import pickle
import json


class MySecretStack(core.Stack):
    
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        
        # code begins
        param1= _ssm.StringParameter(
            self,
            "parm1",
            description="storing config value",
            parameter_name="dbpass",
            string_value="db123",
            tier=_ssm.ParameterTier.STANDARD
        )
        
        secret=_secretmanager.Secret(
            self,
            "mysecret", 
            description="storing db pass",
            secret_name="secretpass"
            
        )
        template={"username":"JonDoe",
                     "user2":"Cena"}
        
        
        #Serialize
        try:
            with open(file="tmplte.pckl",mode="wb") as file:
                tmpl=pickle.dump(template,file)
        except OSError:
            print("could not create file")
            
            
        ifile=open(file="tmplte.pckl",mode="rb") 
        tmlate=pickle.load(ifile)  
        
        print(tmlate)    
          
        
        
        
        
        print(template)
        
        templete_output=_secretmanager.Secret(
            self,
            "tempout",
            description="json dumps to store credentials",
            secret_name="json_secret_store",
            generate_secret_string=_secretmanager.SecretStringGenerator(
                secret_string_template=json.dumps({"username":"JonDoe",
                     "user2":"Cena"}),
                generate_string_key="password"
            )
        )
        
        
        output2= core.CfnOutput(
            self,
            "secretoutp",
            description="secret value",
            value=f"{secret.secret_value}"
        )
            
            
            
    
        
        
        
        output=core.CfnOutput(
            self,
            "output1",
            value=f" param values is {param1.string_value}"
        )
        