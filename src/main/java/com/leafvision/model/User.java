
package com.leafvision.model;

import java.time.LocalDateTime;

public class User {

    private long id;
    private String username;
    private String passwordHash;
    private LocalDateTime createdAt;

    public User(long id, String username, String passwordHash,
                LocalDateTime createdAt) {

        this.id = id;
        this.username = username;
        this.passwordHash = passwordHash;
        this.createdAt = createdAt;
    }

    public long getId() {
        return id;
    }

    public String getUsername() {
        return username;
    }

    public String getPasswordHash() {
        return passwordHash;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }
}
