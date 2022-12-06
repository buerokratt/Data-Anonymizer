package rig.sqlms.datasource;

import org.apache.commons.text.CaseUtils;
import org.springframework.jdbc.core.ColumnMapRowMapper;
import org.springframework.jdbc.core.PreparedStatementCreator;
import org.springframework.jdbc.core.RowMapperResultSetExtractor;
import org.springframework.jdbc.core.namedparam.MapSqlParameterSource;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
import org.springframework.jdbc.support.JdbcUtils;
import org.springframework.lang.Nullable;

import javax.sql.DataSource;
import java.sql.Array;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.util.List;
import java.util.Map;

import static java.util.Collections.emptyList;

public class ResqlJdbcTemplate extends NamedParameterJdbcTemplate {
    public static final JsonColumnMapRowMapper JSON_MAPPER = new JsonColumnMapRowMapper();

    public ResqlJdbcTemplate(DataSource dataSource) {
        super(dataSource);
    }

    public List<Map<String, Object>> queryOrExecute(String query, Map<String, Object> parameters) {
        PreparedStatementCreator psCreator = getPreparedStatementCreator(query, new MapSqlParameterSource(parameters));
        return super.getJdbcOperations().execute(psCreator, preparedStatement -> {
            ResultSetMetaData metaData = preparedStatement.getMetaData();
            if (metaData == null || metaData.getColumnCount() == 0) {
                preparedStatement.execute();
                return emptyList();
            }
            return new RowMapperResultSetExtractor<>(JSON_MAPPER).extractData(preparedStatement.executeQuery());
        });
    }

    private static class JsonColumnMapRowMapper extends ColumnMapRowMapper {

        @Override
        protected String getColumnKey(String columnName) {
            return CaseUtils.toCamelCase(columnName.toLowerCase(), false, '_');
        }

        @Nullable
        @Override
        protected Object getColumnValue(ResultSet rs, int index) throws SQLException {
            Object columnValue = super.getColumnValue(rs, index);
            if (columnValue instanceof Array arrayValue) {
                return arrayValue.getArray();
            }

            return JdbcUtils.getResultSetValue(rs, index);
        }
    }
}
