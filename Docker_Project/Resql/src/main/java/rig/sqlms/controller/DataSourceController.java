package rig.sqlms.controller;

import io.swagger.v3.oas.annotations.Operation;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import rig.sqlms.properties.DataSourceConfigProperties;

import java.util.List;

@RestController
@RequestMapping("/datasources")
@RequiredArgsConstructor
public class DataSourceController {
    private final List<DataSourceConfigProperties> dataSourceConfig;

    @GetMapping
    @Operation(description = "Gets all currently configured datasources (without passwords)")
    public List<DataSourceConfigProperties> findAll() {
        return dataSourceConfig;
    }
}
