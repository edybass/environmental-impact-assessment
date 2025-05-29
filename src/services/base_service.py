"""
Base Service Layer
Foundation for all business logic services

Author: Edy Bassil
Email: bassileddy@gmail.com
"""

from typing import Generic, TypeVar, List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import logging
from abc import ABC, abstractmethod

from src.models import Base
from src.config import get_config

# Generic type for models
ModelType = TypeVar("ModelType", bound=Base)

logger = logging.getLogger(__name__)
config = get_config()


class ServiceException(Exception):
    """Base exception for service layer."""
    def __init__(self, message: str, code: str = "SERVICE_ERROR", details: Dict[str, Any] = None):
        super().__init__(message)
        self.code = code
        self.details = details or {}


class ValidationError(ServiceException):
    """Validation error in service layer."""
    def __init__(self, message: str, field: str = None, details: Dict[str, Any] = None):
        super().__init__(message, "VALIDATION_ERROR", details)
        self.field = field


class NotFoundError(ServiceException):
    """Resource not found error."""
    def __init__(self, resource: str, id: Any):
        super().__init__(f"{resource} with id {id} not found", "NOT_FOUND", {"resource": resource, "id": id})


class UnauthorizedError(ServiceException):
    """Unauthorized access error."""
    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(message, "UNAUTHORIZED")


class BaseService(ABC, Generic[ModelType]):
    """
    Base service class with common CRUD operations.
    Provides transaction management, error handling, and logging.
    """
    
    def __init__(self, model_class: type[ModelType], session: Session):
        self.model_class = model_class
        self.session = session
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def get_by_id(self, id: int, raise_on_not_found: bool = True) -> Optional[ModelType]:
        """
        Get entity by ID.
        
        Args:
            id: Entity ID
            raise_on_not_found: Whether to raise exception if not found
            
        Returns:
            Entity or None
            
        Raises:
            NotFoundError: If entity not found and raise_on_not_found is True
        """
        try:
            entity = self.session.query(self.model_class).filter_by(id=id).first()
            
            if not entity and raise_on_not_found:
                raise NotFoundError(self.model_class.__name__, id)
            
            return entity
        except SQLAlchemyError as e:
            self.logger.error(f"Database error getting {self.model_class.__name__} by id {id}: {e}")
            raise ServiceException(f"Failed to retrieve {self.model_class.__name__}")
    
    def get_all(self, filters: Dict[str, Any] = None, 
                order_by: str = None, 
                limit: int = None, 
                offset: int = None) -> List[ModelType]:
        """
        Get all entities with optional filtering and pagination.
        
        Args:
            filters: Dictionary of filter conditions
            order_by: Column name to order by
            limit: Maximum number of results
            offset: Number of results to skip
            
        Returns:
            List of entities
        """
        try:
            query = self.session.query(self.model_class)
            
            # Apply filters
            if filters:
                for key, value in filters.items():
                    if hasattr(self.model_class, key):
                        query = query.filter(getattr(self.model_class, key) == value)
            
            # Apply ordering
            if order_by:
                if order_by.startswith('-'):
                    # Descending order
                    column = order_by[1:]
                    if hasattr(self.model_class, column):
                        query = query.order_by(getattr(self.model_class, column).desc())
                else:
                    # Ascending order
                    if hasattr(self.model_class, order_by):
                        query = query.order_by(getattr(self.model_class, order_by))
            
            # Apply pagination
            if offset:
                query = query.offset(offset)
            if limit:
                query = query.limit(limit)
            
            return query.all()
        except SQLAlchemyError as e:
            self.logger.error(f"Database error getting all {self.model_class.__name__}: {e}")
            raise ServiceException(f"Failed to retrieve {self.model_class.__name__} list")
    
    def create(self, data: Dict[str, Any], commit: bool = True) -> ModelType:
        """
        Create new entity.
        
        Args:
            data: Entity data
            commit: Whether to commit transaction
            
        Returns:
            Created entity
        """
        try:
            # Validate data
            self._validate_create_data(data)
            
            # Create entity
            entity = self.model_class(**data)
            self.session.add(entity)
            
            if commit:
                self.session.commit()
                self.session.refresh(entity)
            else:
                self.session.flush()
            
            self.logger.info(f"Created {self.model_class.__name__} with id {entity.id}")
            return entity
            
        except ValidationError:
            self.session.rollback()
            raise
        except SQLAlchemyError as e:
            self.session.rollback()
            self.logger.error(f"Database error creating {self.model_class.__name__}: {e}")
            raise ServiceException(f"Failed to create {self.model_class.__name__}")
    
    def update(self, id: int, data: Dict[str, Any], commit: bool = True) -> ModelType:
        """
        Update existing entity.
        
        Args:
            id: Entity ID
            data: Update data
            commit: Whether to commit transaction
            
        Returns:
            Updated entity
        """
        try:
            entity = self.get_by_id(id)
            
            # Validate update data
            self._validate_update_data(data, entity)
            
            # Update fields
            for key, value in data.items():
                if hasattr(entity, key):
                    setattr(entity, key, value)
            
            # Update timestamp if available
            if hasattr(entity, 'updated_at'):
                entity.updated_at = datetime.utcnow()
            
            if commit:
                self.session.commit()
                self.session.refresh(entity)
            else:
                self.session.flush()
            
            self.logger.info(f"Updated {self.model_class.__name__} with id {id}")
            return entity
            
        except (ValidationError, NotFoundError):
            self.session.rollback()
            raise
        except SQLAlchemyError as e:
            self.session.rollback()
            self.logger.error(f"Database error updating {self.model_class.__name__}: {e}")
            raise ServiceException(f"Failed to update {self.model_class.__name__}")
    
    def delete(self, id: int, commit: bool = True) -> bool:
        """
        Delete entity by ID.
        
        Args:
            id: Entity ID
            commit: Whether to commit transaction
            
        Returns:
            True if deleted successfully
        """
        try:
            entity = self.get_by_id(id)
            
            # Check if can be deleted
            self._validate_delete(entity)
            
            self.session.delete(entity)
            
            if commit:
                self.session.commit()
            else:
                self.session.flush()
            
            self.logger.info(f"Deleted {self.model_class.__name__} with id {id}")
            return True
            
        except NotFoundError:
            self.session.rollback()
            raise
        except SQLAlchemyError as e:
            self.session.rollback()
            self.logger.error(f"Database error deleting {self.model_class.__name__}: {e}")
            raise ServiceException(f"Failed to delete {self.model_class.__name__}")
    
    def count(self, filters: Dict[str, Any] = None) -> int:
        """
        Count entities with optional filtering.
        
        Args:
            filters: Dictionary of filter conditions
            
        Returns:
            Count of entities
        """
        try:
            query = self.session.query(self.model_class)
            
            if filters:
                for key, value in filters.items():
                    if hasattr(self.model_class, key):
                        query = query.filter(getattr(self.model_class, key) == value)
            
            return query.count()
        except SQLAlchemyError as e:
            self.logger.error(f"Database error counting {self.model_class.__name__}: {e}")
            raise ServiceException(f"Failed to count {self.model_class.__name__}")
    
    def exists(self, filters: Dict[str, Any]) -> bool:
        """
        Check if entity exists with given filters.
        
        Args:
            filters: Dictionary of filter conditions
            
        Returns:
            True if exists
        """
        return self.count(filters) > 0
    
    def bulk_create(self, data_list: List[Dict[str, Any]], commit: bool = True) -> List[ModelType]:
        """
        Create multiple entities in bulk.
        
        Args:
            data_list: List of entity data
            commit: Whether to commit transaction
            
        Returns:
            List of created entities
        """
        try:
            entities = []
            
            for data in data_list:
                self._validate_create_data(data)
                entity = self.model_class(**data)
                entities.append(entity)
            
            self.session.bulk_save_objects(entities, return_defaults=True)
            
            if commit:
                self.session.commit()
            else:
                self.session.flush()
            
            self.logger.info(f"Bulk created {len(entities)} {self.model_class.__name__} entities")
            return entities
            
        except ValidationError:
            self.session.rollback()
            raise
        except SQLAlchemyError as e:
            self.session.rollback()
            self.logger.error(f"Database error bulk creating {self.model_class.__name__}: {e}")
            raise ServiceException(f"Failed to bulk create {self.model_class.__name__}")
    
    def transaction(self, func, *args, **kwargs):
        """
        Execute function within a transaction.
        
        Args:
            func: Function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Function result
        """
        try:
            result = func(*args, **kwargs)
            self.session.commit()
            return result
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Transaction failed: {e}")
            raise
    
    # Abstract methods to be implemented by subclasses
    @abstractmethod
    def _validate_create_data(self, data: Dict[str, Any]) -> None:
        """Validate data for creation. Raise ValidationError if invalid."""
        pass
    
    @abstractmethod
    def _validate_update_data(self, data: Dict[str, Any], entity: ModelType) -> None:
        """Validate data for update. Raise ValidationError if invalid."""
        pass
    
    def _validate_delete(self, entity: ModelType) -> None:
        """Validate if entity can be deleted. Raise ServiceException if not."""
        pass


class CachedService(BaseService[ModelType]):
    """
    Service with caching capabilities.
    Requires Redis or similar cache backend.
    """
    
    def __init__(self, model_class: type[ModelType], session: Session, cache_ttl: int = 300):
        super().__init__(model_class, session)
        self.cache_ttl = cache_ttl  # Cache time-to-live in seconds
        self._cache = {}  # Simple in-memory cache for demo
    
    def _get_cache_key(self, method: str, *args, **kwargs) -> str:
        """Generate cache key."""
        return f"{self.model_class.__name__}:{method}:{args}:{kwargs}"
    
    def _get_from_cache(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        # In production, use Redis or similar
        return self._cache.get(key)
    
    def _set_cache(self, key: str, value: Any) -> None:
        """Set value in cache."""
        # In production, use Redis with TTL
        self._cache[key] = value
    
    def _invalidate_cache(self, pattern: str = None) -> None:
        """Invalidate cache entries."""
        if pattern:
            # In production, use pattern matching
            keys_to_delete = [k for k in self._cache.keys() if pattern in k]
            for key in keys_to_delete:
                del self._cache[key]
        else:
            self._cache.clear()
    
    def get_by_id(self, id: int, raise_on_not_found: bool = True) -> Optional[ModelType]:
        """Get entity by ID with caching."""
        cache_key = self._get_cache_key("get_by_id", id)
        cached = self._get_from_cache(cache_key)
        
        if cached is not None:
            return cached
        
        entity = super().get_by_id(id, raise_on_not_found)
        if entity:
            self._set_cache(cache_key, entity)
        
        return entity
    
    def create(self, data: Dict[str, Any], commit: bool = True) -> ModelType:
        """Create entity and invalidate cache."""
        entity = super().create(data, commit)
        self._invalidate_cache(self.model_class.__name__)
        return entity
    
    def update(self, id: int, data: Dict[str, Any], commit: bool = True) -> ModelType:
        """Update entity and invalidate cache."""
        entity = super().update(id, data, commit)
        self._invalidate_cache(self.model_class.__name__)
        return entity
    
    def delete(self, id: int, commit: bool = True) -> bool:
        """Delete entity and invalidate cache."""
        result = super().delete(id, commit)
        self._invalidate_cache(self.model_class.__name__)
        return result