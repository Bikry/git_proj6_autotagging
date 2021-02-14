from flask import Flask,render_template,url_for,request
import pandas as pd
import numpy as np
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import re, nltk
import bs4 as bs
from bs4 import BeautifulSoup as bs
from nltk import word_tokenize
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import stopwords
#import pattern3
#from pattern3.en import lemma, lexeme


# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

@app.route('/')
def welcome():
    return render_template('form.html')


@app.route('/result', methods=['POST'])
def result():
    title = request.form["title"]
    question = request.form["question"]
    titquest=conc(title,question)

    entry= auto_tags(titquest)
    print(entry)
    entry=entry

    return render_template('result1.html', entrer= entry)


def conc(x,y):
    return str(x) + ' ' + str(y)

def delete_code(text):
    pos=text.find('<code>')
    while pos!=-1:
        ender=text.find(u'</code>')
        text=text.replace(text[pos:ender+7],' ')
        pos=text.find('<code>')
    return text

def delete_html(text):
    return bs(text, 'lxml').get_text()

def delete_indesirable_chars_and_stopwords(text):
    text=str(text)
    text=text.lower()

    text = re.sub(r"\n's", " ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"can't", "can not ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text=re.sub("c\+\+","cplpl", text)
    text=re.sub("c2+","cplpl", text)
    text=re.sub("c#","csharp", text)
    text=re.sub("\.net","dotnet", text)
    text=re.sub("d3\.js","dthreejs", text)
    text=re.sub("[^a-zA-Z0-9]"," ", text)
    text=re.sub("cplpl","c++", text)
    text=re.sub("csharp","c#", text)
    text=re.sub("dthreejs","d3\.js", text)

    return text

def isInteger(stringToTest):
    try:
# We cannot use  isinstance(stringToTest, int) ...
        int(stringToTest)
        return True
    except:
        return False

def remove_num_and_stops(text):
    """Map POS tag to first character lemmatize() accepts"""
    #try :
    return " ".join([word for word in text.split(' ')
                        if (isInteger(word)==False and word not in Stopwords)])

Stopwords=list(set((stopwords.words('english'))))
list_to_avoid = ['AT', 'IN', 'CC', 'PP', 'WD','RB', 'JJ', 'DT', 'CD','RB', 'VB']


#def get_wordnet_pos(text):
#    """Map POS tag to first character lemmatize() accepts"""
#    return " ".join([lemma(nltk.pos_tag([str(word)])[0][0]).lower() for word in text.split()
#                        if (nltk.pos_tag([word])[0][1][:2].upper() not in list_to_avoid) and (word not in Stopwords)])




#parser = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
top_tags = ['python-requests', 'neural-network', 'post', 'flutter-layout', 'websocket', 'python-3.7', 'optimization', 'pyqt5', 'expo', 'android-fragments', 'xcode11', 'xpath', 'pycharm', 'hadoop', 'electron', 'uwp', 'gcc', 'react-router', 'd3.js', 'iis', 'sqlalchemy', 'java-8', 'random', 'unix', 'spring-security', 'data-structures', 'while-loop', 'azure-active-directory', 'inheritance', 'automation', 'gitlab', 'promise', 'dependency-injection', 'oauth-2.0', 'vector', 'encryption', 'lambda', 'awk', 'hive', 'plsql', 'animation', 'django-views', 'multidimensional-array', 'outlook', 'dockerfile', 'perl', 'angular7', 'text', 'google-chrome-extension', 'time', 'uitableview', 'arraylist', 'vuetify.js', 'ffmpeg', 'junit', 'stored-procedures', 'selenium-chromedriver', 'groovy', 'search', 'tomcat', 'indexing', 'arduino', 'redis', 'nuxt.js', 'jwt', 'graph', 'import', 'select', 'jenkins-pipeline', 'canvas', 'terminal', 'ssh', 'dom', 'charts', 'cmd', 'opengl', 'sed', 'redirect', 'caching', 'cookies', 'flexbox', 'mariadb', 'struct', 'django-forms', 'group-by', 'datatables', 'methods', 'azure-functions', 'nativescript', 'split', 'audio', 'session', 'button', 'jdbc', 'memory', 'windows-10', 'facebook', 'time-series', 'c++17', 'blazor', 'xamarin.android', 'mobile', 'winapi', 'sharepoint', 'terraform', 'merge', 'pygame', 'types', 'serialization', 'google-app-engine', 'xslt', 'yaml', 'raspberry-pi', 'replace', 'jmeter', 'https', 'mvvm', 'vue-component', 'laravel-6', 'build', 'react-native-android', 'asp.net-core-3.0', 'error-handling', 'events', 'scipy', 'pyqt', 'request', 'installation', 'postman', 'ms-word', 'scrapy', 'firefox', 'google-analytics', 'delphi', 'datatable', 'azure-pipelines', 'pandas-groupby', 'razor', 'conv-neural-network', 'multiprocessing', 'three.js', 'sequelize.js', 'foreach', 'jsp', 'julia', 'swagger', 'django-templates', 'macos-catalina', 'soap', 'fetch', 'data-science', 'tensorflow2.0', 'discord.js', 'webview', 'iframe', 'computer-vision', 'gatsby', 'firebase-cloud-messaging', 'module', '.net-core-3.0', 'linked-list', 'chart.js', 'botframework', 'jackson', 'makefile', 'google-api', 'deployment', 'next.js', 'microsoft-graph-api', 'socket.io', 'leaflet', 'symfony4', 'video', 'r-markdown', 'neo4j', 'highcharts', 'iphone', 'plotly', 'airflow', 'amazon-dynamodb', 'snowflake-cloud-data-platform', 'ubuntu-18.04', 'continuous-integration', 'asp.net-core-webapi', 'encoding', 'functional-programming', 'proxy', 'package', 'design-patterns', 'statistics', 'plugins', 'dynamic', 'java-stream', 'array-formulas', 'automated-tests', 'push-notification', 'openssl', 'compiler-errors', 'printing', 'command-line', 'ruby-on-rails-5', 'conditional-statements', 'android-intent', 'parallel-processing', 'visual-c++', 'web-services', 'ssis', 'react-navigation', 'xamarin.ios', 'model', 'vuex', 'reporting-services', 'lua', 'mockito', 'progressive-web-apps', 'rabbitmq', 'tcp', 'checkbox', 'microservices', 'count', 'routing', 'rstudio', 'puppeteer', 'ionic3', 'frontend', 'mongodb-query', 'safari', 'concurrency', 'kivy', 'hyperledger-fabric', 'asp.net-core-mvc', 'parameters', 'visual-studio-2017', 'json.net', 'twilio', 'listview', 'mocking', 'collections', 'browser', 'internet-explorer', 'nested', 'cron', 'fonts', 'active-directory', 'dialogflow-es', 'enums', 'jupyter', 'google-colaboratory', 'google-drive-api', 'colors', 'gitlab-ci', 'cors', 'data.table', 'environment-variables', 'x86', 'lstm', 'unicode', 'file-upload', 'google-cloud-storage', 'boto3', 'amazon-cloudformation', 'reflection', 'sas', 'scroll', 'dns', 'google-kubernetes-engine', 'android-room', 'oauth', 'data-binding', 'oracle11g', 'tidyverse', 'pytest', 'tree', 'sum', 'dax', 'discord', 'cypress', 'conda', 'observable', 'download', 'cassandra', 'uicollectionview', 'routes', 'thymeleaf', 'containers', 'servlets', 'syntax', 'duplicates', 'hash', 'flask-sqlalchemy', 'view', 'interface', 'constructor', 'directory', 'regression', 'scripting', 'path', 'azure-web-app-service', 'linux-kernel', 'vim', 'angular6', 'db2', 'compilation', 'prometheus', 'nestjs', 'dll', 'nuget', 'seaborn', 'aggregation-framework', 'timestamp', 'jasmine', 'service', 'swift5', 'devops', 'boost', 'python-imaging-library', 'mysqli', 'html-table', 'phpmyadmin', 'create-react-app', 'python-3.6', 'pagination', 'tuples', 'jinja2', 'apache-flink', 'composer-php', 'odoo', 'binary', 'androidx', 'laravel-5.8', 'azure-sql-database', 'bluetooth', 'pivot', 'retrofit2', 'ssl-certificate', 'format', 'aws-sdk', 'stream', 'drop-down-menu', 'navigation', 'permissions', 'google-play', 'amazon-redshift', 'stripe-payments', 'jsf', '3d', 'entity-framework-6', 'transactions', 'callback', 'cryptography', 'get', 'latex', 'notifications', 'configuration', 'datepicker', 'operating-system', 'spring-data', 'amazon-cognito', 'hyperlink', 'database-design', 'tfs', 'stack', 'casting', 'momentjs', 'appium', 'css-grid', 'ngrx', 'c++14', 'protractor', 'hashmap', 'floating-point', 'layout', 'utf-8', 'base64', 'subprocess', 'wso2', 'command-line-interface', 'grpc', 'kendo-ui', 'keycloak', 'iterator', 'kibana', 'centos', 'memory-management', 'azure-cosmosdb', 'logstash', 'vue-router', 'dependencies', 'grep', 'aws-api-gateway', 'jsx', 'magento2', 'enzyme', 'antd', 'cucumber', 'char', 'databricks', 'android-activity', 'components', 'solr', 'wcf', 'kubernetes-helm', 'architecture', 'amazon-elastic-beanstalk', 'authorization', 'append', 'type-conversion', 'salesforce', 'jar', 'spring-webflux', 'state', 'vscode-settings', 'data-visualization', 'build.gradle', 'scope', 'xampp', 'bots', 'range', 'activerecord', 'sonarqube', 'angular-reactive-forms', 'static', 'console', 'url-rewriting', 'apollo', 'identityserver4', 'timer', 'apache-poi', 'yii2', 'eslint', 'apache-camel', 'node-modules', 'camera', 'iteration', 'kotlin-coroutines', 'sap', 'google-oauth', 'fortran', 'jakarta-ee', 'nullpointerexception', 'pyspark-sql', 'webforms', 'arm', 'dropdown', 'blazor-server-side', 'formatting', 'graphics', 'controller', 'time-complexity', 'numbers', 'triggers', 'markdown', 'ldap', 'html5-canvas', 'mocha', 'gulp', 'office365', 'admob', 'crash', 'spring-batch', 'linear-regression', 'clang', 'migration', 'virtual-machine', 'dataset', 'memory-leaks', 'shopify', 'boolean', 'reference', 'vbscript', 'service-worker', 'twitter', 'netbeans', 'uikit', 'cocoapods', 'bluetooth-lowenergy', 'css-selectors', 'facebook-graph-api', 'material-design', 'javascript-objects', 'aggregate', 'codeigniter-3', 'google-sheets-query', 'orm', 'google-sheets-api', 'gpu', 'doctrine', 'celery', 'web-applications', 'razor-pages', 'queue', 'gdb', 'python-asyncio', 'cloud', 'character-encoding', 'babel', 'apache-nifi', 'bitbucket', 'object-detection', 'attributes', 'f#', 'linker', 'calendar', 'timezone', 'modal-dialog', 'retrofit', 'fullcalendar', 'pdo', 'web-crawler',  'nosql', 'signalr', 'ejs', 'grafana', 'segmentation-fault', 'office-js', 'annotations', 'core-data', 'return', 'msbuild', 'android-livedata', 'openpyxl', 'certificate', 'spacy', 'robotframework', 'pivot-table', 'xmlhttprequest', 'amazon-ecs', 'qml', 'laravel-blade', 'android-gradle-plugin', 'android-sqlite', 'typo3', 'openshift', 'maps', 'styled-components', 'centos7', 'jq', 'gmail', 'react-router-dom', 'gson', 'switch-statement', 'output', 'hyperledger', 'mapbox', 'webrtc', 'cypher', 'paypal', 'firebase-storage', 'aws-glue', 'tf.keras', 'embedded', 'properties', 'bigdata', 'responsive-design', 'token', 'mips', 'header', 'int', 'hdfs', 'elixir', 'numpy-ndarray', 'ssms', 'arguments', 'android-webview', 'bootstrap-modal', 'dask', 'datagridview', 'qt5', 'amazon-rds', 'chatbot', 'process', 'geolocation', 'foreign-keys', 'smtp', 'processing', 'google-chrome-devtools', 'dom-events', 'junit5', 'upload', 'hex', 'sql-update', 'udp', 'microsoft-teams', 'jboss', 'serial-port', 'webdriver', 'combobox', 'localhost', 'keyboard', 'sdk', 'classification', 'integration-testing', 'bokeh', 'wkwebview', 'onclick', 'jvm', 'concatenation', 'python-import', 'autocomplete', 'cakephp', 'integer', 'xml-parsing', 'youtube', 'asp.net-identity', 'language-lawyer', 'azure-data-factory', 'nltk', 'wordpress-theming', 'debian', 'find', 'mysql-workbench', 'copy', 'zip', 'primefaces', 'initialization', 'reverse-proxy', 'openid-connect', 'windows-subsystem-for-linux', 'pyinstaller', 'sapui5', 'amazon-iam', 'pyspark-dataframes', 'oracle-apex', 'lodash', 'karma-jasmine', 'label', 'io', 'pipe', 'histogram', 'drag-and-drop', 'save', 'magento', 'subquery', 'sympy', 'background', 'odata', 'crystal-reports', 'widget', 'svelte', 'protocol-buffers', 'sql-server-2012', 'stl', 'set', 'apache-kafka-streams', 'odbc', 'ag-grid', 'azure-databricks', 'tidyr', 'automapper', 'bar-chart', 'ruby-on-rails-6', 'android-constraintlayout', 'react-native-ios', 'google-cloud-dataflow', 'apache-beam', 'networkx', 'binding', 'powerpoint', 'django-admin', 'twig', 'insert', 'discord.py', 'sharepoint-online', 'export-to-csv', 'http-headers', 'internet-explorer-11', 'phpunit', 'jenkins-plugins', 'cocoa', 'kubernetes-ingress', 'apply', 'testng', 'apollo-client', 'ckeditor', 'rubygems', 'x86-64', 'geometry', 'mqtt', 'material-components-android', 'sh', 'kernel', 'recurrent-neural-network', 'flutter-dependencies', 'server-side-rendering', 'match', 'jquery-ui', 'local-storage', 'dynamics-crm']
#word_top_tags='python-requestsneural-networkpostflutter-layoutwebsocketpython-3.7optimizationpyqt5expoandroid-fragmentsxcode11xpathpycharmhadoopelectronuwpgccreact-routerd3.jsiissqlalchemyjava-8randomunixspring-securitydata-structureswhile-loopazure-active-directoryinheritanceautomationgitlabpromisedependency-injectionoauth-2.0vectorencryptionlambdaawkhiveplsqlanimationdjango-viewsmultidimensional-arrayoutlookdockerfileperlangular7textgoogle-chrome-extensiontimeuitableviewarraylistvuetify.jsffmpegjunitstored-proceduresselenium-chromedrivergroovysearchtomcatindexingarduinoredisnuxt.jsjwtgraphimportselectjenkins-pipelinecanvasterminalsshdomchartscmdopenglsedredirectcachingcookiesflexboxmariadbstructdjango-formsgroup-bydatatablesmethodsazure-functionsnativescriptsplitaudiosessionbuttonjdbcmemorywindows-10facebooktime-seriesc++17blazorxamarin.androidmobilewinapisharepointterraformmergepygametypesserializationgoogle-app-enginexsltyamlraspberry-pireplacejmeterhttpsmvvmvue-componentlaravel-6buildreact-native-androidasp.net-core-3.0error-handlingeventsscipypyqtrequestinstallationpostmanms-wordscrapyfirefoxgoogle-analyticsdelphidatatableazure-pipelinespandas-groupbyrazorconv-neural-networkmultiprocessingthree.jssequelize.jsforeachjspjuliaswaggerdjango-templatesmacos-catalinasoapfetchdata-sciencetensorflow2.0discord.jswebviewiframecomputer-visiongatsbyfirebase-cloud-messagingmodule.net-core-3.0linked-listchart.jsbotframeworkjacksonmakefilegoogle-apideploymentnext.jsmicrosoft-graph-apisocket.ioleafletsymfony4videor-markdownneo4jhighchartsiphoneplotlyairflowamazon-dynamodbsnowflake-cloud-data-platformubuntu-18.04continuous-integrationasp.net-core-webapiencodingfunctional-programmingproxypackagedesign-patternsstatisticspluginsdynamicjava-streamarray-formulasautomated-testspush-notificationopensslcompiler-errorsprintingcommand-lineruby-on-rails-5conditional-statementsandroid-intentparallel-processingvisual-c++web-servicesssisreact-navigationxamarin.iosmodelvuexreporting-servicesluamockitoprogressive-web-appsrabbitmqtcpcheckboxmicroservicescountroutingrstudiopuppeteerionic3frontendmongodb-querysafariconcurrencykivyhyperledger-fabricasp.net-core-mvcparametersvisual-studio-2017json.nettwiliolistviewmockingcollectionsbrowserinternet-explorernestedcronfontsactive-directorydialogflow-esenumsjupytergoogle-colaboratorygoogle-drive-apicolorsgitlab-cicorsdata.tableenvironment-variablesx86lstmunicodefile-uploadgoogle-cloud-storageboto3amazon-cloudformationreflectionsasscrolldnsgoogle-kubernetes-engineandroid-roomoauthdata-bindingoracle11gtidyversepytesttreesumdaxdiscordcypresscondaobservabledownloadcassandrauicollectionviewroutesthymeleafcontainersservletssyntaxduplicateshashflask-sqlalchemyviewinterfaceconstructordirectoryregressionscriptingpathazure-web-app-servicelinux-kernelvimangular6db2compilationprometheusnestjsdllnugetseabornaggregation-frameworktimestampjasmineserviceswift5devopsboostpython-imaging-librarymysqlihtml-tablephpmyadmincreate-react-apppython-3.6paginationtuplesjinja2apache-flinkcomposer-phpodoobinaryandroidxlaravel-5.8azure-sql-databasebluetoothpivotretrofit2ssl-certificateformataws-sdkstreamdrop-down-menunavigationpermissionsgoogle-playamazon-redshiftstripe-paymentsjsf3dentity-framework-6transactionscallbackcryptographygetlatexnotificationsconfigurationdatepickeroperating-systemspring-dataamazon-cognitohyperlinkdatabase-designtfsstackcastingmomentjsappiumcss-gridngrxc++14protractorhashmapfloating-pointlayoututf-8base64subprocesswso2command-line-interfacegrpckendo-uikeycloakiteratorkibanacentosmemory-managementazure-cosmosdblogstashvue-routerdependenciesgrepaws-api-gatewayjsxmagento2enzymeantdcucumberchardatabricksandroid-activitycomponentssolrwcfkubernetes-helmarchitectureamazon-elastic-beanstalkauthorizationappendtype-conversionsalesforcejarspring-webfluxstatevscode-settingsdata-visualizationbuild.gradlescopexamppbotsrangeactiverecordsonarqubeangular-reactive-formsstaticconsoleurl-rewritingapolloidentityserver4timerapache-poiyii2eslintapache-camelnode-modulescameraiterationkotlin-coroutinessapgoogle-oauthfortranjakarta-eenullpointerexceptionpyspark-sqlwebformsarmdropdownblazor-server-sideformattinggraphicscontrollertime-complexitynumberstriggersmarkdownldaphtml5-canvasmochagulpoffice365admobcrashspring-batchlinear-regressionclangmigrationvirtual-machinedatasetmemory-leaksshopifybooleanreferencevbscriptservice-workertwitternetbeansuikitcocoapodsbluetooth-lowenergycss-selectorsfacebook-graph-apimaterial-designjavascript-objectsaggregatecodeigniter-3google-sheets-queryormgoogle-sheets-apigpudoctrineceleryweb-applicationsrazor-pagesqueuegdbpython-asynciocloudcharacter-encodingbabelapache-nifibitbucketobject-detectionattributesf#linkercalendartimezonemodal-dialogretrofitfullcalendarpdoweb-crawlernannosqlsignalrejsgrafanasegmentation-faultoffice-jsannotationscore-datareturnmsbuildandroid-livedataopenpyxlcertificatespacyrobotframeworkpivot-tablexmlhttprequestamazon-ecsqmllaravel-bladeandroid-gradle-pluginandroid-sqlitetypo3openshiftmapsstyled-componentscentos7jqgmailreact-router-domgsonswitch-statementoutputhyperledgermapboxwebrtccypherpaypalfirebase-storageaws-gluetf.kerasembeddedpropertiesbigdataresponsive-designtokenmipsheaderinthdfselixirnumpy-ndarrayssmsargumentsandroid-webviewbootstrap-modaldaskdatagridviewqt5amazon-rdschatbotprocessgeolocationforeign-keyssmtpprocessinggoogle-chrome-devtoolsdom-eventsjunit5uploadhexsql-updateudpmicrosoft-teamsjbossserial-portwebdrivercomboboxlocalhostkeyboardsdkclassificationintegration-testingbokehwkwebviewonclickjvmconcatenationpython-importautocompletecakephpintegerxml-parsingyoutubeasp.net-identitylanguage-lawyerazure-data-factorynltkwordpress-themingdebianfindmysql-workbenchcopyzipprimefacesinitializationreverse-proxyopenid-connectwindows-subsystem-for-linuxpyinstallersapui5amazon-iampyspark-dataframesoracle-apexlodashkarma-jasminelabeliopipehistogramdrag-and-dropsavemagentosubquerysympybackgroundodatacrystal-reportswidgetsvelteprotocol-bufferssql-server-2012stlsetapache-kafka-streamsodbcag-gridazure-databrickstidyrautomapperbar-chartruby-on-rails-6android-constraintlayoutreact-native-iosgoogle-cloud-dataflowapache-beamnetworkxbindingpowerpointdjango-admintwiginsertdiscord.pysharepoint-onlineexport-to-csvhttp-headersinternet-explorer-11phpunitjenkins-pluginscocoakubernetes-ingressapplytestngapollo-clientckeditorrubygemsx86-64geometrymqttmaterial-components-androidshkernelrecurrent-neural-networkflutter-dependenciesserver-side-renderingmatchjquery-uilocal-storagedynamics-crm'
word_top_tags=''
for i in top_tags:
    word_top_tags=word_top_tags+str(i)

def lemmatize_text(text, selected_postags):
    lemmatizer = nltk.stem.WordNetLemmatizer()
    doc = parser(text)
    output = []
    for token in doc:
        if (str(token) in top_tags or str(token) in word_top_tags) and (len(token)>1 or str(token)=='c' or str(token)=='r') and (str(token)!='lt') and (str(token)!='gt') :
            output.append(str(token))
        elif token.pos_ in selected_postags:
            if token.lemma_ not in ['-PRON-'] :
             output.append(token.lemma_)
            else:
                output.append(' ')
    output = ' '.join(output)
    return output

def preprocess(text):
    text=delete_code(text)
    text=delete_html(text)
    text=remove_num_and_stops(text)
    text = delete_indesirable_chars_and_stopwords(text)
#    print(text)
#    text= get_wordnet_pos(text)
    return  text

vectorizer_X_=pickle.load(open('vectorizer_1000.pkl', 'rb'))
lda_ = pickle.load(open('lda.pkl', 'rb'))
clf_svm = pickle.load(open('model_svm_voca_1000.pkl', 'rb'))
clf_pagg = pickle.load(open('model_paggcl_voca_1000.pkl', 'rb'))
vectorizer_ex=pickle.load(open('vectorizer_1000.pkl', 'rb'))




def similar_tags(tags, delimitor,number , threshold):
    result=''
    similar_tags=[]
    scores=[]
    tags_list=[]
    nb=len(tags.split(delimitor))
    if nb==0:
        similar_tags=''
    else:

        tags_list = tags.split(delimitor)

        for i in tags_list:
            try :
                for m,n in model_word_vec.most_similar(i):
                    similar_tags.append(m)
                    scores.append(n)
            except:
                pass

    dict_sim=pd.DataFrame({"tag": similar_tags, "score": scores})
    dict_sim.drop_duplicates(subset=['tag'],inplace =True)
    dict_sim=dict_sim[dict_sim['score']>=threshold]
    dict_sim =dict_sim.sort_values(by='score', ascending=False)

    if nb>=number:
        result=''
    else:
       if number-nb>len(dict_sim)-1:
           numb=len(dict_sim)-1
       else:
           numb=number-nb

       for i in range(numb):
         result=result+delimitor+ str(dict_sim.iloc[i,0])
    return dict_sim

def recommend_tags_lda_unit_without_embedding(text, vector, lda_model, nbr):


    ''' Recomendation system for stackoverflow posts based on a lda model,
    it returns up to 5 tags.
    Parameters:
    text: the stackoverflow post of user
    X_train: data to fit the model with
    '''

    textstr=text
    text = text.split()
    n_topics = nbr
    threshold = 0.2
    list_scores_topics = []
    list_words = []
    used = set()
    list_words_scores=[]
    list_scores=[]
    text_tfidf = vector.transform(text)


    text_projection = lda_model.transform(text_tfidf)
    feature_names = vector.get_feature_names()
    lda_components = lda_model.components_ / lda_model.components_.sum(axis=1)[:, np.newaxis] # normalization

    for topic in range(n_topics):
        topic_score = text_projection[0][topic]

        for (word_idx, word_score) in zip(lda_components[topic].argsort()[:-5:-1], sorted(lda_components[topic])[:-5:-1]):
            score_top = topic_score
            score_word = word_score

            if score_top >= threshold:
                list_scores_topics.append(score_top)
                list_words.append(feature_names[word_idx])
                list_words_scores.append(score_word)
                list_scores.append(score_word*score_top)
                used.add(feature_names[word_idx])

    #results = [tag for (y,tag) in sorted(zip(list_scores,list_words, list_scores_topics), key=lambda pair: pair[0], reverse=True)]
    #unique_results = [x for x in results if x not in used] # get only unique tags
    tags = ",".join(i for i in list_words )

    df_lda = pd.DataFrame({'words':list_words, 'score_topic': list_scores_topics, 'score_words': list_words_scores})

    return list_words, list_scores_topics,list_words_scores, list_scores

def recommand_tags_lda_without_embedding(text, vector, lda_model, nbr):
    text = preprocess(text)
    text_l = text.split()
    print(text_l)
    list_words=[]
    list_scoret=[]
    list_scorew=[]
    list_scoreg=[]

    for text_ in text_l:
        list_words_,list_scoret_,list_scorew_, list_scoreg_ =recommend_tags_lda_unit_without_embedding(text_, vectorizer_X_, lda_,10)
        list_words+=list_words_
        list_scoret+=list_scoret_
        list_scorew+=list_scorew_
        list_scoreg+=list_scoreg_

    df_lda_tot=  pd.DataFrame({'words':list_words, 'score_topic': list_scoret, 'score_words': list_scorew,
                               'score_total': list_scoreg})
    df_lda_tot= df_lda_tot.sort_values(by='score_total', ascending = False)
    tags=[]
    for i in range(len(df_lda_tot)):
        if  df_lda_tot.iloc[i,0] not in tags and len(tags)< (nbr):
            tags.append(df_lda_tot.iloc[i,0])

    tags_="|".join(i for i in tags)
    return tags_


def supervised(text):
    Question_=preprocess(text)
    classes = vectorizer_ex.get_feature_names()
    X=text
    X_tfidf_ex = vectorizer_ex.transform(X.split())
    y_pred=clf_svm.predict(X_tfidf_ex )
    y_pred1=clf_pagg.predict(X_tfidf_ex )
    yy=pd.DataFrame(data=y_pred+y_pred1, columns=classes)
    yy
    cl_sel=[]
    cl_sum=[]
    for i in yy.columns:
        if yy[i].sum()!=0:
            cl_sel.append(i)
            cl_sum.append(yy[i].sum())
    return "|".join(t for t in cl_sel)

def auto_tags(texte):
    t = str(supervised(texte))
    t_ = t.split('|')

    r = recommand_tags_lda_without_embedding(texte, vectorizer_X_, lda_, 5)
    r_=r.split('|')

    s_=t_ + r_
    s_=list(set(s_))
    return '|'.join(y for y in s_)
