package rig.sqlms.datasource;

import lombok.experimental.UtilityClass;
import org.springframework.util.Assert;
import org.springframework.web.context.annotation.ApplicationScope;

@UtilityClass
@ApplicationScope
public class DataSourceContextHolder {
    private static final ThreadLocal<String> context = new ThreadLocal<>();

    public static void setDataSourceName(String dataSourceName) {
        Assert.notNull(dataSourceName, "dataSourceName cannot be null");
        context.set(dataSourceName);
    }

    public static String getDataSourceName() {
        return context.get();
    }

    public static void clearDataSourceName() {
        context.remove();
    }
}
