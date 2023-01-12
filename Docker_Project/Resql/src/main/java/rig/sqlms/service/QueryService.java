package rig.sqlms.service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import rig.sqlms.datasource.DataSourceContextHolder;
import rig.sqlms.datasource.ResqlJdbcTemplate;
import rig.sqlms.exception.UnknownDataSourceNameException;
import rig.sqlms.model.SavedQuery;
import rig.sqlms.properties.DataSourceConfigProperties;

import java.util.List;
import java.util.Map;
import java.util.Objects;

@Slf4j
@Service
@RequiredArgsConstructor
public class QueryService {
    private final List<DataSourceConfigProperties> configProperties;
    private final SavedQueryService savedQueryService;
    private final ResqlJdbcTemplate resqlJdbcTemplate;

    public List<Map<String, Object>> execute(String queryName, Map<String, Object> parameters) {
        SavedQuery savedQuery = savedQueryService.get(queryName);
        setDatabaseContext(savedQuery.dataSourceName());
        return resqlJdbcTemplate.queryOrExecute(savedQuery.query(), parameters);
    }

    private void setDatabaseContext(String dataSourceName) {
        configProperties.stream()
                .map(DataSourceConfigProperties::getName)
                .filter(propertyDataSourceName -> Objects.equals(dataSourceName, propertyDataSourceName))
                .findFirst()
                .ifPresentOrElse(DataSourceContextHolder::setDataSourceName,
                        () -> {
                            throw new UnknownDataSourceNameException(dataSourceName);
                        }
                );
    }
}
