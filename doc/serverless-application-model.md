# Serverless Application Model

##### 版本 2019-11-10

本文件中的 “一定”，“不一定”，“必填”，“将要”，“最好不要”，“应该”，“不应该”，“推荐”，“可能”，和 “可选” 按照 [RFC 2119](http://www.ietf.org/rfc/rfc2119.txt) 中的描述进行解释。

## 介绍

FS 是用于在京东云上定义 serverless 应用的模型。

Serverless 应用是由事件触发功能组成的应用。一个典型的 serverless 应用由一个或多个由诸如向 [京东云 OSS](https://docs.jdcloud.com/cn/object-storage-service/product-overview) 上传对象，向[京东云队列服务](https://docs.jdcloud.com/cn/queue-service/product-overview) 发送消息以及API 操作等事件触发的京东云函数计算组成。这些函数可以独立使用。也可以利用其它资源，例如京东云 OSS 的 buckets和[京东云缓存 Redis](https://docs.jdcloud.com/cn/jcs-for-redis/product-overview) 。最基本的 serverless 应用可以只有一个函数。

## 规范

### 格式

京东云 FS 用通过 [YAML](http://yaml.org/spec/1.1/) 格式的模板文件来描述 serverless 应用。

模板文件必须在文档根节点中包含一个值为 `JDCloud::Serverless-2019-11-10` 的 `Transform` 部分。

- [Resource 类型](#resource-类型)
- [事件源类型](#事件源类型)
- [Property 类型](#property-类型)

### 示例：京东云 FS 模板

```yaml
ROSTemplateFormatVersion: '2015-09-01'
Transform: 'JDCloud::Serverless-2019-11-10'
Resources:
  function-test:                                  # 待创建函数名称
    Type: 'JDCloud::Serverless::Function'   
    Properties:                             
      Handler: index.handler                
      Timeout: 10
      MemorySize: 128
      Runtime: python2.7
      Description: test
      CodeUri: './'
      Env:
        'key': 'value'
      Role: role-test                             # 角色名称
      Policies: policy-test                       # 权限策略
      VPCConfig:
        Vpc: vpc-name                             # vpc 名称
        Subnet: subnet-name                       # subnet 名称
      LogConfig:
        LogSet: log-set-name                      # 日志集名称
        LogTopic: log-topic-name                  # 日志主题名称
      Events:
        oss-trigger-test:                         # oss 触发器名称
          Type: 'JDCloud::Serverless::OSS'
          Properties:
            BucketName: test-bucket
            Events:
              - oss:ObjectCreated:*
              - oss:ObjectRemoved:DeleteObject
            Filter:
              Key:
                Prefix: src/
                Suffix: .jpg
        api-group-test:                           # api group 名称
          Type: 'JDCloud::Serverless::ApiGroup'
          Properties:
            Stage: Online
            Version: 0.0.1  #Api版本
          api-test:                               # api 名称
            Type: 'JDCloud::Serverless::Api'
            Properties:
              Path: /test
              Method: post
        jqs-test:                                 # jqs 队列名称
          Type: 'JDCloud::Serverless::JQS'
          Properties:
            BatchSize: 10
```

京东云 FS 中的所有属性名称都**区分大小写**。

### Resource 类型

- [JDCloud::Serverless::Function](#jdcloudserverlessfunction)

#### JDCloud::Serverless::Function

描述函数及其绑定的事件源。

###### 属性

属性名称 | 类型 | 描述
---|:---:|---
Handler | `string` | **必填。** 处理函数的调用入口。
Runtime | `string` | **必填。** 运行时环境。可选值为：nodejs6、nodejs8、python2.7、python3.6、python3.7。
CodeUri | `string` | **必填。** 代码位置。支持 file、dir、zip等形式，更多信息[参考](#codeuri)。
Description | `string` | 函数的描述。
MemorySize | `integer` | 每次函数执行分配的内存大小，单位是 MB，默认为 128（MB）。
Timeout | `integer` | 处理函数在被终止之前可以运行的最长时间，单位是秒，默认为 3 秒。
Env | [环境变量对象](#环境变量对象) | 为函数配置[环境变量](https://docs.jdcloud.com/cn/function-service/env-variable)。
Events | [事件源对象](#事件源对象) | 用于定义触发此函数的事件。
Role | `string` | 使用一个 RAM 角色的 Name 为函数指定执行角色。 如果忽略，将为函数创建一个[默认的角色](#默认-Role)。
Policies | `string` <span>&#124;</span> `string` 列表  | 函数需要的京东云管理的 RAM policies 或 RAM policy 文档的名称，将会被附加到该函数的默认角色上。如果设置了 Role 属性，则该属性会被忽略。
VpcConfig | [Vpc 配置对象](#vpc-配置对象) | 允许函数访问 vpc 内的服务。
LogConfig | [Log 配置对象](#log-配置对象) | 允许函数执行的日志存储在日志服务中。
Description | `string` | 函数的描述。

##### 示例：JDCloud::Serverless::Function

```yaml

  MyFunction:                               # function 名称
    Type: 'JDCloud::Serverless::Function'
    Properties:
      Handler: index.handler
      Runtime: python3.7
      CodeUri: './' 
      Description: Python3.7 Function Test
      MemorySize: 512
      Timeout: 10
```

### 事件源类型

- [OSS](#OSS)
- [APIG](#APIG)
- [JQS](#JQS)

#### OSS

描述类型为 [OSS 触发器](https://docs.jdcloud.com/cn/function-service/oss-tirgger) 的对象。

##### 属性

属性名称 | 类型 | 描述
---|:---:|---
Events| `array` | **必填。** 为 OSS 端触发函数执行的事件，比如参数为 ["oss:ObjectCreated:PutObject", "oss:ObjectCreated:PutSymlink"] 等...
BucketName| `stirng` | **必填。** 为 OSS 中对应的 bucket 名称。
Filter   | `object` | **必填。** 为 OSS 对象过滤参数，满足过滤条件的 OSS 对象才可以触发函数，包含一个配置属性 key，表示过滤器支持过滤的对象键 (key)。 
Key | [OSS Key 对象](#OSS-Key-配置对象) | **必填。** 过滤器支持过滤的对象键

##### 示例：OSS 事件源对象

```yaml
oss-trigger-test:                           # oss 触发器名称
    Type: 'JDCloud::Serverless::OSS'        
     Properties:
      BucketName: ossBucketName             # oss bucket 名称
      Events:
        - oss:ObjectCreated:*
        - oss:ObjectRemoved:DeleteObject
      Filter: 
        Key:
          Prefix: src/
          Suffix: .jpg
```

#### APIG

描述类型为 [APIGATEWAY 触发器](https://docs.jdcloud.com/cn/function-service/apig-tigger) 的对象。

##### 属性

属性名称 | 类型 | 描述
---|:---:|---
Stage| `string` | **必填。** 发布阶段的名称，API 网关用作调用统一资源标识符（URI）中的第一个路径段。可选值为：test、preview、online。默认如果为新 API 服务时为 release，已有 API 服务时为test。
Version| `stirng` | **必填。** Api分组版本号。默认为0.0.1。
Api   | [Api 对象](#Api-对象) | **必填。** ApiGroup下的Api。 


##### 示例：APIGATEWAY 事件源对象

```yaml
api-group-test:                           # ApiGroup 名称
  Type: 'JDCloud::Serverless::ApiGroup'
  Properties:
    Stage: Online                         # ApiGroup 待发布环境
    Version: 0.0.1                        # ApiGroup 版本
    api-test:                             # Api 名称
      Type: 'JDCloud::Serverless::Api'
      Properties:
        Path: /test                       # Api 子路径
        Method: post                      # Api 方法
```

#### JQS

描述类型为 [JQS 触发器](https://docs.jdcloud.com/cn/queue-service/core-concepts) 的对象。

##### 属性

属性名称 | 类型 | 描述
---|:---:|---
BatchSize| `integer` | **必填。** 为jqs触发器一次性从消息队列中获取消息数量。取值范围1-10。

##### 示例：JQS 事件源对象

```yaml
jqs-test:                             # jqs 队列名称
  Type: 'JDCloud::Serverless::JQS'
  Properties:
    BatchSize: 10
```

### Property 类型

- [事件源对象](#事件源对象)

#### 事件源对象

描述触发函数的事件源的对象。

##### 属性

属性名称 | 类型 | 描述
---|:---:|---
Type | `string` | **必填。** 事件类型。 事件源类型包括 [Api](#APIG)、[JQS](#jqs) 等。有关所有类型的更多信息， 请参阅 [事件源类型](#事件源类型)。
Properties | * | **必填。** 描述此事件映射属性的对象。必须符合定义的 `类型` 。有关所有类型的更多信息，请参阅 [事件源类型](#事件源类型)。

##### 示例：事件源对象

```yaml

Type: 'JDCloud::Serverless::OSS'        
Properties:
  BucketName: ossBucketName             
  Events:
    - oss:ObjectCreated:*
    - oss:ObjectRemoved:DeleteObject
  Filter: 
    Key:
      Prefix: src/
      Suffix: .jpg
```

#### Vpc 配置对象

Vpc 配置对象包含的属性包括： `VpcName` 和 `SubnetName` 属性。它们所代表的含义[参考](https://docs.jdcloud.com/cn/virtual-private-cloud/core-concepts)。

示例：

```
VpcConfig:
    VpcName: 'vpc-test'
    SubnetName: 'subnet-test'
```

#### Log 配置对象

Log 配置对象用来指定函数执行的日志将要存储到的日志服务。

Log 配置对象可配置的属性包括：`LogSet`、`LogTopic`。其中 `LogSet`、`LogTopic` 的概念与日志服务中的概念一致。更多信息[参考](https://docs.jdcloud.com/cn/log-service/logsetmanagement)。

示例：

```
LogConfig:
    LogSet: log-set-test
    LogTopic: log-topic-test
```

#### 环境变量对象

环境变量可以配置一系列的键值对。

示例：

```
Env:
  'key1': 'value1'
  'key2': 'value2'
```

#### CodeUri

CodeUri 用来指定代码存储的位置，它可以用来指定：

>文件（file）：`CodeUri: hello.js`
目录（dir）：`CodeUri: ./`
压缩包（zip）：`CodeUri: hello.zip`

#### OSS Key 配置对象

Key 配置对象的属性包括： `Prefix` 和 `Suffix` 属性。它们所代表的含义分别为：匹配前缀和匹配后缀。

示例：

```
Key:
  Prefix: src/
  Suffix: .jpg
```

#### Api 对象

Api 对象的属性包括： `Method` 和 `Path` 属性。触发Function的Api网关的HTTP Method和子路径。

##### 属性

属性名称 | 类型 | 描述
---|:---:|---
Mehod | `string` | **必填。** HTTP 请求子路径。
Path | `string` | **必填。** HTTP 请求方法，可选值为：ANY、GET、POST、PUT、DELETE、HEAD，默认值为ANY。

示例：

```
api-test:
  Type: 'JDCloud::Serverless::Api'
  Properties: 
    Method: GET
    Path: /test

```

#### 默认 Role

默认 role 会被生成的场景包括：指定了 policies 的时候或者服务配置了 vpc、jqs 等明确需要特定权限的属性时候。

这样设计的原因是：

1. 因为生成 role 用户需要为子用户分配一个很大的权限，非必要场景下，我们尽可能不去生成这个默认 role，尽可能避免用户的子用户权限不够情况。
2. 一般这个 role 的使用场景是用来调用其他云服务的，即使生成了默认的 role，但是没有指定 policies 也是没有意义的，因为不会有相应的权限。
3. ram 有角色数量的限制。
