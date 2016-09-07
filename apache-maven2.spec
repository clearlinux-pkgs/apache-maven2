Name     : apache-maven2
Version  : 2.2.1
Release  : 1
URL      : https://archive.apache.org/dist/maven/source/apache-maven-2.2.1-src.tar.gz
Source0  : https://archive.apache.org/dist/maven/source/apache-maven-2.2.1-src.tar.gz
Summary  : No detailed summary available
Group    : Development/Tools
License  : Apache-2.0
Patch1: maven2-2.2.1-update-tests.patch
Patch2: maven2-2.2.1-unshade.patch
Patch3: maven2-2.2.1-default-resolver-pool-size.patch
Patch4: maven2-2.2.1-strip-jackrabbit-dep.patch
Patch5: maven2-2.2.1-migrate-to-plexus-containers-container-default.patch
BuildRequires : apache-maven
BuildRequires : apache-maven2
BuildRequires : javapackages-tools
BuildRequires : jdk-aether
BuildRequires : jdk-aopalliance
BuildRequires : jdk-apache-parent
BuildRequires : jdk-apache-resource-bundles
BuildRequires : jdk-atinject
BuildRequires : jdk-base64coder
BuildRequires : jdk-bsh
BuildRequires : jdk-cdi-api
BuildRequires : jdk-commons-cli
BuildRequires : jdk-commons-codec
BuildRequires : jdk-commons-collections
BuildRequires : jdk-commons-compress
BuildRequires : jdk-commons-io
BuildRequires : jdk-commons-lang
BuildRequires : jdk-commons-lang3
BuildRequires : jdk-commons-logging
BuildRequires : jdk-doxia
BuildRequires : jdk-doxia-integration-tools
BuildRequires : jdk-doxia-sitetools
BuildRequires : jdk-enforcer
BuildRequires : jdk-guava
BuildRequires : jdk-guice
BuildRequires : jdk-httpcomponents-client
BuildRequires : jdk-httpcomponents-core
BuildRequires : jdk-jackson-annotations
BuildRequires : jdk-jackson-core
BuildRequires : jdk-jackson-databind
BuildRequires : jdk-jdependency
BuildRequires : jdk-jdom
BuildRequires : jdk-jsoup
BuildRequires : jdk-jsr-305
BuildRequires : jdk-log4j
BuildRequires : jdk-maven-archiver
BuildRequires : jdk-maven-artifact-resolver
BuildRequires : jdk-maven-common-artifact-filters
BuildRequires : jdk-maven-compiler-plugin
BuildRequires : jdk-maven-dependency-tree
BuildRequires : jdk-maven-filtering
BuildRequires : jdk-maven-invoker
BuildRequires : jdk-maven-jar-plugin
BuildRequires : jdk-maven-javadoc-plugin
BuildRequires : jdk-maven-parent
BuildRequires : jdk-maven-plugin-testing
BuildRequires : jdk-maven-plugin-tools
BuildRequires : jdk-maven-remote-resources-plugin
BuildRequires : jdk-maven-reporting-api
BuildRequires : jdk-maven-resources-plugin
BuildRequires : jdk-maven-shade-plugin
BuildRequires : jdk-maven-shared-incremental
BuildRequires : jdk-maven-shared-utils
BuildRequires : jdk-modello
BuildRequires : jdk-objectweb-asm
BuildRequires : jdk-plexus-archiver
BuildRequires : jdk-plexus-build-api
BuildRequires : jdk-plexus-cipher
BuildRequires : jdk-plexus-classworlds
BuildRequires : jdk-plexus-compiler
BuildRequires : jdk-plexus-containers
BuildRequires : jdk-plexus-i18n
BuildRequires : jdk-plexus-interactivity
BuildRequires : jdk-plexus-interpolation
BuildRequires : jdk-plexus-io
BuildRequires : jdk-plexus-resources
BuildRequires : jdk-plexus-sec-dispatcher
BuildRequires : jdk-plexus-utils
BuildRequires : jdk-plexus-velocity
BuildRequires : jdk-sisu
BuildRequires : jdk-slf4j
BuildRequires : jdk-snakeyaml
BuildRequires : jdk-snappy-java
BuildRequires : jdk-surefire
BuildRequires : jdk-velocity
BuildRequires : jdk-wagon
BuildRequires : jdk-xbean
BuildRequires : jdk-xmlunit
BuildRequires : lxml
BuildRequires : openjdk-dev
BuildRequires : python3
BuildRequires : six
BuildRequires : xmvn

%description
-------------------------------------------------------------------------------
Bootstrapping Maven
-------------------------------------------------------------------------------

%prep
%setup -q -n apache-maven-2.2.1
%patch1
%patch2
%patch3 -p1
%patch4 -p1
%patch5 -p1

for nobuild in apache-maven maven-artifact-test \
maven-compat maven-core maven-plugin-api \
maven-plugin-parameter-documenter maven-reporting \
maven-repository-metadata maven-script \
maven-error-diagnostics; do
python3 /usr/share/java-utils/pom_editor.py pom_disable_module $nobuild
done
python3 /usr/share/java-utils/mvn_package.py :maven __noinstall
python3 /usr/share/java-utils/mvn_file.py ":{*}" maven/@1
python3 /usr/share/java-utils/mvn_compat_version.py ":maven-{artifact,model,settings}" \
2.0.2 2.0.6 2.0.7 2.0.8 2.2.1
python3 /usr/share/java-utils/pom_editor.py pom_remove_dep :backport-util-concurrent
python3 /usr/share/java-utils/pom_editor.py pom_remove_dep :backport-util-concurrent maven-artifact-manager
sed -i s/edu.emory.mathcs.backport.// `find -name DefaultArtifactResolver.java`

%build
python3 /usr/share/java-utils/mvn_build.py   -f -s -- -P all-models

%install
xmvn-install  -R .xmvn-reactor -n maven2 -d %{buildroot} 

%files
%defattr(-,root,root,-)
