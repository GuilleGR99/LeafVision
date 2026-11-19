
package com.leafvision.model;

import java.math.BigDecimal;
import java.time.LocalDateTime;

public class Analysis {

    private long id;
    private long userId;
    private String classId;
    private String commonName;
    private String scientificName;
    private BigDecimal confidence;
    private String referenceImage;
    private LocalDateTime createdAt;

    public Analysis(long id, long userId, String classId,
                    String commonName, String scientificName,
                    BigDecimal confidence, String referenceImage,
                    LocalDateTime createdAt) {

        this.id = id;
        this.userId = userId;
        this.classId = classId;
        this.commonName = commonName;
        this.scientificName = scientificName;
        this.confidence = confidence;
        this.referenceImage = referenceImage;
        this.createdAt = createdAt;
    }

    public long getId() {
        return id;
    }

    public long getUserId() {
        return userId;
    }

    public String getClassId() {
        return classId;
    }

    public String getCommonName() {
        return commonName;
    }

    public String getScientificName() {
        return scientificName;
    }

    public BigDecimal getConfidence() {
        return confidence;
    }

    public String getReferenceImage() {
        return referenceImage;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }
}
