# app/routes/search.py
from flask import Blueprint, request, jsonify
from http import HTTPStatus
from typing import Optional, Dict, Any
from app.services.search import SearchService
from app.utils.validation import validate_search_params
from config import Config
        
def create_search_blueprint(database):
    """Creates and returns the search blueprint with configured routes"""
    
    search_bp = Blueprint('search', __name__)
    
    search_service = SearchService(
        database=database,
        cohere_api_key=Config.COHERE_KEY
    )
    
    @search_bp.route('/text', methods=['POST'])
    async def text_search():
        """
        Text-based search endpoint
        
        Request body:
        {
            "query": "software engineers from Berkeley",
            "limit": 10,
            "offset": 0
        }
        """
        try:
            data = request.get_json()
            
            # Validate request parameters
            validation_result = validate_search_params(data)
            if not validation_result['valid']:
                return jsonify({
                    "status": "error",
                    "message": validation_result['message']
                }), HTTPStatus.BAD_REQUEST
                
            # Extract parameters
            query = data.get('query')
            limit = data.get('limit', 10)
            offset = data.get('offset', 0)
            
            # Perform search
            results = search_service.search_by_text(
                query=query,
                k=limit
            )
            
            # Apply pagination
            paginated_results = results[offset:offset + limit]
            
            return jsonify({
                "status": "success",
                "results": paginated_results,
                "count": len(paginated_results),
                "total": len(results),
                "has_more": len(results) > (offset + limit)
            }), HTTPStatus.OK
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), HTTPStatus.INTERNAL_SERVER_ERROR

    @search_bp.route('/similar/<profile_id>', methods=['GET'])
    async def similar_profiles(profile_id: str):
        """
        Find similar profiles endpoint
        
        URL Parameters:
        - limit: Number of similar profiles to return
        """
        try:
            limit = request.args.get('limit', default=5, type=int)
            
            results = search_service.suggest_similar_profiles(
                profile_id=profile_id,
                k=limit
            )
            
            return jsonify({
                "status": "success",
                "results": results,
                "count": len(results)
            }), HTTPStatus.OK
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), HTTPStatus.INTERNAL_SERVER_ERROR

    return search_bp