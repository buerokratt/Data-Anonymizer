package rig.sqlms.datasource;

import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.tuple.Pair;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.jdbc.DataSourceBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import rig.sqlms.properties.DataSourceConfigProperties;

import java.util.ArrayList;
import java.util.List;

import static java.util.stream.Collectors.toMap;

@Slf4j
@Configuration
public class DataSourceConfiguration {

    @Bean(name = "dataSource")
    public RoutingDataSource dataSource(List<DataSourceConfigProperties> dataSourceConfig) {
        log.info("Initializing datasource: {}", dataSourceConfig.stream()
                .map(DataSourceConfigProperties::getName)
                .toList());
        RoutingDataSource dataSource = new RoutingDataSource();

        dataSource.setTargetDataSources(dataSourceConfig.stream()
                .map(config -> Pair.of(config.getName(), DataSourceBuilder.create()
                        .driverClassName(config.getDriverClassName())
                        .url(config.getJdbcUrl())
                        .username(config.getUsername())
                        .password(config.getPassword())
                        .build()))
                .collect(toMap(Pair::getKey, Pair::getValue)));

        return dataSource;
    }

    @Bean
    public ResqlJdbcTemplate resqlJdbcTemplate(RoutingDataSource dataSource) {
        return new ResqlJdbcTemplate(dataSource);
    }

    @Bean(name = "dataSourceConfig")
    @ConfigurationProperties(prefix = "sqlms.datasources")
    public List<DataSourceConfigProperties> readProperties() {
        return new ArrayList<>();
    }
}
