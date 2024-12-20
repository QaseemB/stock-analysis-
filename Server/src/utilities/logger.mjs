import winston from 'winston';  // Default import

const { createLogger, format, transports } = winston;  // Destructure from the winston object

export const logger = createLogger({
  level: 'info',
  format: format.combine(
    format.timestamp(),
    format.json(),
  ),
  defaultMeta: { service: 'user-service' },
  transports: [
    // Write all logs with importance level of `error` or higher to `error.log`
    new transports.File({ filename: 'error.log', level: 'error' }),

    // Write all logs with importance level of `info` or higher to `combined.log`
    new transports.File({ filename: 'combined.log' }),

    // Add console transport for non-production environments
    ...(process.env.NODE_ENV !== 'production' ? [
      new transports.Console({
        format: format.simple(),
      })
    ] : []),
  ],
});
