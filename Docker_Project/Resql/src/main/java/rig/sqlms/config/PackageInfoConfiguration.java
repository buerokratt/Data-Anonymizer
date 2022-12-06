package rig.sqlms.config;

import lombok.Getter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;

@Getter
@Configuration
@PropertySource("classpath:heartbeat.properties")
public class PackageInfoConfiguration {

    @Value("${app.name:}")
    private String appName;

    @Value("${app.version:}")
    private String version;

    @Value("${app.packaging.time:}")
    private long packagingTime;

}
