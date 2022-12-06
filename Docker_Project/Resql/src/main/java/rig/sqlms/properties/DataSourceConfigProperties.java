package rig.sqlms.properties;

import com.fasterxml.jackson.annotation.JsonIgnore;
import io.swagger.v3.oas.annotations.Hidden;
import lombok.Data;

import java.io.Serializable;

@Data
public class DataSourceConfigProperties implements Serializable {
    private String name;
    private String jdbcUrl;
    private String username;
    @JsonIgnore
    @Hidden
    private String password;
    private String driverClassName;
}
